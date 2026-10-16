import re
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from botocore.exceptions import ClientError

from src.dto.api_result import ApiResult
from src.infra.db import get_connection
from src.infra.tebi import get_bucket_name, get_s3_client
from src.repository.report_repository import ReportRepository
from src.repository.report_media_repository import ReportMediaRepository
from src.enums.types_report import TypesReport

_ALLOWED_ID = re.compile(r"^[A-Za-z0-9_-]{1,36}$")
_MEDIA_GROUPS = {
    "external_compressor", "internal_compressor", "air_filter", "oil_filter",
    "air_oil_separator", "pre_coalescing", "post_coalescing", "belts", "hoses",
    "compressor_nameplate", "dryer_nameplate", "motor_nameplate",
    "lubrication_nameplate", "unit_nameplate",
}


class OrdemServiceAttachmentService:
    def __init__(self):
        self.s3 = get_s3_client()
        self.bucket_name = get_bucket_name()
        self.repository = ReportRepository()
        self.media_repository = ReportMediaRepository()

    def _get_owned_report(self, order_service_id: str, client_id: str):
        conn = get_connection()
        try:
            return self.repository.get_by_id_reference_and_id_client(
                order_service_id, client_id, conn
            )
        finally:
            conn.close()

    @staticmethod
    def _validate_media(items: Iterable, report_type: str):
        signature_count = 0
        seen_ids = set()

        for item in items:
            if not _ALLOWED_ID.fullmatch(item.id):
                raise ValueError("Identificador de mídia inválido")
            if item.id in seen_ids:
                raise ValueError("Há mídias repetidas na solicitação")
            seen_ids.add(item.id)
            if report_type == TypesReport.NEEDS_ASSESSMENT.value:
                if item.type != "photo" or item.group not in _MEDIA_GROUPS:
                    raise ValueError("Categoria de mídia inválida para o levantamento")
            elif item.group is not None:
                raise ValueError("Categoria de mídia inválida para a Ordem de Serviço")
            if item.type == "signature":
                if item.content_type != "image/png":
                    raise ValueError("Assinatura deve ser PNG")
                signature_count += 1

        if signature_count > 1:
            raise ValueError("O relatório pode ter somente uma assinatura")

    @staticmethod
    def _prefix(client_id: str, order_service_id: str) -> str:
        return f"clients/{client_id}/reports/{order_service_id}/"

    def _object_key(self, client_id: str, order_service_id: str, item, report_type: str) -> str:
        prefix = self._prefix(client_id, order_service_id)
        if report_type == TypesReport.NEEDS_ASSESSMENT.value:
            extension = ".png" if item.content_type == "image/png" else ".jpg"
            return f"{prefix}needs-assessment/{item.group}/{item.id}{extension}"
        # Keep the historical object key format for existing service orders.
        extension = ".png" if item.type == "signature" else ".jpg"
        return f"{prefix}{item.type}s/{item.id}{extension}"

    def generate_upload_urls(self, order_service_id: str, client_id: str, items):
        report = self._get_owned_report(order_service_id, client_id)
        if not report:
            result = ApiResult.not_found_result("Relatório não encontrado")
            return result.to_dict(), result.status_code

        try:
            self._validate_media(items, report.type)
        except ValueError as error:
            result = ApiResult.validation_error_result(str(error))
            return result.to_dict(), result.status_code

        uploads = []
        for item in items:
            object_key = self._object_key(client_id, order_service_id, item, report.type)
            upload_url = self.s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": object_key,
                    "ContentType": item.content_type,
                },
                ExpiresIn=600,
            )
            uploads.append(
                {
                    "id": item.id,
                    "type": item.type,
                    "object_key": object_key,
                    "upload_url": upload_url,
                }
            )

        result = ApiResult.success_result(
            data={"uploads": uploads},
            message="URLs de upload geradas",
        )
        return result.to_dict(), result.status_code

    def finalize(self, order_service_id: str, client_id: str, items, base_media=None):
        report = self._get_owned_report(order_service_id, client_id)
        if not report:
            result = ApiResult.not_found_result("Relatório não encontrado")
            return result.to_dict(), result.status_code

        try:
            self._validate_media(items, report.type)
            expected_prefix = self._prefix(client_id, order_service_id)
            for item in items:
                expected_key = self._object_key(client_id, order_service_id, item, report.type)
                if item.object_key != expected_key or not item.object_key.startswith(expected_prefix):
                    raise ValueError("Chave de mídia inválida")
        except ValueError as error:
            result = ApiResult.validation_error_result(str(error))
            return result.to_dict(), result.status_code

        conn = get_connection()
        try:
            self.media_repository.lock_report(order_service_id, conn)
            previous_media = self.media_repository.get_report_media(order_service_id, conn)
            if self.media_repository.foreign_media_ids([item.id for item in items], order_service_id, conn):
                result = ApiResult.validation_error_result("ID de mídia pertence a outro relatório")
                return result.to_dict(), result.status_code
            if report.type == TypesReport.NEEDS_ASSESSMENT.value:
                if base_media is None:
                    result = ApiResult.error_result("Versão das fotos ausente", status_code=409)
                    return result.to_dict(), result.status_code
                current = sorted(
                    (item["id"], item["object_key"], item["updated_at"].isoformat())
                    for item in previous_media
                )
                expected = sorted(
                    (item.id, item.object_key, item.updated_at)
                    for item in base_media
                )
                if current != expected:
                    result = ApiResult.error_result(
                        "As fotos foram alteradas em outro aparelho. Sincronize antes de reenviar.",
                        status_code=409,
                    )
                    return result.to_dict(), result.status_code
            verified = {(item["id"], item["object_key"]) for item in previous_media}
            new_media = [item for item in items if (item.id, item.object_key) not in verified]
            if new_media:
                # Previously verified objects do not need another remote HEAD on each sync.
                with ThreadPoolExecutor(max_workers=min(4, len(new_media))) as executor:
                    list(executor.map(
                        lambda item: self.s3.head_object(Bucket=self.bucket_name, Key=item.object_key),
                        new_media,
                    ))
            self.media_repository.replace_report_media(order_service_id, items, conn)
            manifest = self.media_repository.get_manifests([order_service_id], conn).get(order_service_id, [])
        except ClientError:
            result = ApiResult.validation_error_result(
                "Uma ou mais mídias não foram encontradas no storage"
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

        active_keys = {item.object_key for item in items}
        stale_keys = [
            item["object_key"]
            for item in previous_media
            if item["object_key"] not in active_keys
        ]

        if stale_keys:
            try:
                self.s3.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={"Objects": [{"Key": key} for key in stale_keys]},
                )
            except ClientError:
                # O cadastro já está consistente. O objeto remanescente não será
                # exposto pela API e pode ser limpo em uma tentativa posterior.
                pass

        result = ApiResult.success_result(
            data={"media_manifest": manifest},
            message="Mídias do relatório sincronizadas",
        )
        return result.to_dict(), result.status_code

    def get_media(self, order_service_id: str, client_id: str):
        if not self._get_owned_report(order_service_id, client_id):
            result = ApiResult.not_found_result("Relatório não encontrado")
            return result.to_dict(), result.status_code

        conn = get_connection()
        try:
            media = self.media_repository.get_report_media(order_service_id, conn)
        finally:
            conn.close()

        for item in media:
            item["download_url"] = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": item["object_key"],
                },
                ExpiresIn=300,
            )

        result = ApiResult.success_result(
            data={"media": media},
            message="Mídias do relatório obtidas",
        )
        return result.to_dict(), result.status_code
