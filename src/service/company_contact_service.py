import re
import uuid

from botocore.exceptions import ClientError

from src.dto.api_result import ApiResult
from src.infra.db import get_connection
from src.infra.tebi import get_bucket_name, get_s3_client
from src.repository.company_contact_repository import CompanyContactRepository

_ALLOWED_ID = re.compile(r"^[A-Za-z0-9_-]{1,36}$")


class CompanyContactService:
    def __init__(self):
        self.repository = CompanyContactRepository()
        self.s3 = None
        self.bucket_name = None

    def _storage(self):
        if self.s3 is None:
            self.s3 = get_s3_client()
            self.bucket_name = get_bucket_name()
        return self.s3, self.bucket_name

    def _ensure_company(self, company_id, client_id, conn):
        return self.repository.company_is_owned(company_id, client_id, conn)

    @staticmethod
    def _serialize(contact, s3=None, bucket_name=None):
        result = dict(contact)
        for key in ("created_at", "updated_at", "signature_updated_at"):
            if hasattr(result.get(key), "isoformat"):
                result[key] = result[key].isoformat()
        if result.get("signature_object_key") and s3 and bucket_name:
            result["signature_download_url"] = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": result["signature_object_key"]},
                ExpiresIn=600,
            )
        return result

    def get_all(self, company_id, client_id):
        conn = get_connection()
        try:
            if not self._ensure_company(company_id, client_id, conn):
                return ApiResult.not_found_result("Empresa não encontrada").to_dict(), 404
            contacts = self.repository.get_all(company_id, conn)
            s3 = bucket = None
            if any(contact.get("signature_object_key") for contact in contacts):
                s3, bucket = self._storage()
            return ApiResult.success_result(
                data=[self._serialize(contact, s3, bucket) for contact in contacts],
                message="Clientes da empresa encontrados",
            ).to_dict(), 200
        finally:
            conn.close()

    def upsert(self, company_id, dto, client_id):
        conn = get_connection()
        try:
            if not self._ensure_company(company_id, client_id, conn):
                return ApiResult.not_found_result("Empresa não encontrada").to_dict(), 404
            contact_id = dto.id or str(uuid.uuid4())
            if not _ALLOWED_ID.fullmatch(contact_id):
                return ApiResult.validation_error_result("Identificador de cliente inválido").to_dict(), 422
            contact = {
                "id": contact_id,
                "name": dto.name.strip(),
                "email": dto.email.strip() if dto.email else None,
                "phone": dto.phone.strip() if dto.phone else None,
            }
            self.repository.upsert(company_id, contact, conn)
            saved = self.repository.get_owned(company_id, contact_id, conn)
            if not saved:
                return ApiResult.validation_error_result(
                    "Identificador de cliente já pertence a outra empresa"
                ).to_dict(), 422
            return ApiResult.success_result(
                data=self._serialize(saved), message="Cliente salvo com sucesso"
            ).to_dict(), 200
        finally:
            conn.close()

    def delete(self, company_id, contact_id, client_id):
        conn = get_connection()
        try:
            if not self._ensure_company(company_id, client_id, conn):
                return ApiResult.not_found_result("Empresa não encontrada").to_dict(), 404
            if not self.repository.deactivate(company_id, contact_id, conn):
                return ApiResult.not_found_result("Cliente não encontrado").to_dict(), 404
            return ApiResult.success_result(data=None, message="Cliente removido com sucesso").to_dict(), 200
        finally:
            conn.close()

    @staticmethod
    def _signature_key(client_id, company_id, contact_id):
        return f"clients/{client_id}/companies/{company_id}/contacts/{contact_id}/signature.png"

    def get_signature_upload_url(self, company_id, contact_id, dto, client_id):
        conn = get_connection()
        try:
            if not self._ensure_company(company_id, client_id, conn):
                return ApiResult.not_found_result("Empresa não encontrada").to_dict(), 404
            if not self.repository.get_owned(company_id, contact_id, conn):
                return ApiResult.not_found_result("Cliente não encontrado").to_dict(), 404
            s3, bucket = self._storage()
            object_key = self._signature_key(client_id, company_id, contact_id)
            upload_url = s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={"Bucket": bucket, "Key": object_key, "ContentType": dto.content_type},
                ExpiresIn=600,
            )
            return ApiResult.success_result(
                data={"object_key": object_key, "upload_url": upload_url},
                message="URL de upload da assinatura gerada",
            ).to_dict(), 200
        finally:
            conn.close()

    def complete_signature(self, company_id, contact_id, dto, client_id):
        expected_key = self._signature_key(client_id, company_id, contact_id)
        if dto.object_key != expected_key:
            return ApiResult.validation_error_result("Chave de assinatura inválida").to_dict(), 422
        conn = get_connection()
        try:
            if not self._ensure_company(company_id, client_id, conn):
                return ApiResult.not_found_result("Empresa não encontrada").to_dict(), 404
            if not self.repository.get_owned(company_id, contact_id, conn):
                return ApiResult.not_found_result("Cliente não encontrado").to_dict(), 404
            s3, bucket = self._storage()
            try:
                s3.head_object(Bucket=bucket, Key=dto.object_key)
            except ClientError:
                return ApiResult.validation_error_result("Assinatura não encontrada no storage").to_dict(), 422
            self.repository.update_signature(
                company_id, contact_id, dto.object_key, dto.content_type, dto.size_bytes, conn
            )
            saved = self.repository.get_owned(company_id, contact_id, conn)
            return ApiResult.success_result(
                data=self._serialize(saved, s3, bucket), message="Assinatura salva com sucesso"
            ).to_dict(), 200
        finally:
            conn.close()
