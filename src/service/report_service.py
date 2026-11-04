import math

from botocore.exceptions import ClientError

from src.dto.api_result import ApiResult
from src.dto.report_sync_dto import ReportSyncDTO
from src.model.ordem_service import OrdemService
from src.model.needs_assessment import NeedsAssessment
from src.enums.types_report import TypesReport
from src.dto.report_reference_dto import ReportReferenceDTO
from src.infra.db import get_connection
from src.dto.report_dto import ReportDTO
from src.enums.status_report import StatusReport
from src.model.report import Report
from src.repository.report_repository import ReportRepository
from src.repository.needs_assessment_repository import NeedsAssessmentRepository
from src.repository.report_media_repository import ReportMediaRepository
from src.repository.company_contact_repository import CompanyContactRepository
from src.repository.technician_repository import TechnicianRepository
from src.infra.tebi import get_bucket_name, get_s3_client
from typing import Any, Dict, List, Optional

def _format_report_datetime(value: Any) -> Optional[str]:
    return OrdemService.format_datetime(value)


class ReportService:

    def __init__(self):
        self.report_repository = ReportRepository()
        self.needs_repository = NeedsAssessmentRepository()
        self.media_repository = ReportMediaRepository()
        self.company_contact_repository = CompanyContactRepository()
        self.technician_repository = TechnicianRepository()
        self.s3 = get_s3_client()
        self.bucket_name = get_bucket_name()

    def _delete_bucket_objects(self, object_keys: List[str]):
        """Remove objects before deleting their database manifest.

        S3-compatible APIs accept at most 1,000 keys per request.  An explicit
        error response is also needed because delete_objects can report errors
        in its payload without raising a ClientError.
        """
        for start in range(0, len(object_keys), 1000):
            keys = object_keys[start:start + 1000]
            response = self.s3.delete_objects(
                Bucket=self.bucket_name,
                Delete={"Objects": [{"Key": key} for key in keys]},
            )
            if response.get("Errors"):
                raise RuntimeError("O storage recusou a remoção de uma ou mais fotos")

    def _validate_order_closing_contact(self, order_service, conn):
        """A contact can only close an order for its own company.

        Orders created before this feature have no contact and remain valid.
        """
        if not order_service.closing_contact_id:
            return True
        return bool(self.company_contact_repository.get_owned(
            order_service.id_company, order_service.closing_contact_id, conn
        ))

    def _validate_order_technicians(self, order_service, client_id, conn):
        ids = list(dict.fromkeys(order_service.closing_technician_ids or []))
        return len(ids) == len(self.technician_repository.owned_ids(ids, client_id, conn))

    def get_all(self, app_user_id: str):
        conn = get_connection()

        reports = self.report_repository.get_all(app_user_id, conn)

        result = ApiResult.success_result(
            data=reports,
            message="Reports fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def get_all_ids(self, id_client: str):
        conn = get_connection()

        ids = self.report_repository.get_all_ids_by_status(
            id_client=id_client,
            status=StatusReport.IN_PROGRESS.value,
            conn=conn
        )

        result = ApiResult.success_result(
            data=ids,
            message="Report IDs fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def get_by_id(self, id: str, id_client: str):
        conn = get_connection()
        try:

            report = self.report_repository.get_by_id_client_and_id(id, id_client, conn)

            if report is None:
                return ApiResult.error_result(
                    message="Report not found",
                    status_code=422
                ).to_dict(), 422

            reference = None

            match report.type:
                case TypesReport.ORDEM_SERVICE.value:
                    reference = self.report_repository.get_reference_ordem_service(report.id_reference, conn)
                case TypesReport.NEEDS_ASSESSMENT.value:
                    reference = self.needs_repository.get_by_id(report.id_reference, conn)
                    if reference:
                        reference = NeedsAssessment.serialize(reference)

            result = ApiResult.success_result(
                data=reference,
                message="Reference fetched successfully",
                status_code=200
            )

            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def create(self, report_dto: ReportDTO, app_user_id: str, id_client: str):
        conn = get_connection()
        try:

            report_is_exists = self.report_repository.get_by_id_reference_and_id_client(report_dto.id_reference, id_client, conn)

            if report_is_exists:
                data = {
                    "is_exists": True
                }

                result = ApiResult.success_result(
                    data=data,
                    message="Report already exists",
                    status_code=200
                )

                return result.to_dict(), result.status_code

            report = Report(
                id=report_dto.id,
                id_reference=report_dto.id_reference,
                type=report_dto.type.value,
                status=StatusReport.IN_PROGRESS.value,
                id_client=id_client,
                id_app_user=app_user_id
            )

            report_reference = self.report_repository.create(report, conn)

            data = {
                "report": report_reference.to_dict(),
                "is_exists": False
            }

            result = ApiResult.success_result(
                data=data,
                message="Report created successfully",
                status_code=200
            )

            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def create_reference(self, report_reference_dto: ReportReferenceDTO, id_client: str):
        conn = get_connection()
        try:

            report = self.report_repository.get_by_id_reference_and_id_client(report_reference_dto.id, id_client, conn)

            if not report:
                return {"message": "Report not found"}, 422

            match report.type:
                case TypesReport.ORDEM_SERVICE.value:
                    if report_reference_dto.order_service is None:
                        return {"message": "Dados da Ordem de Serviço ausentes"}, 422
                    model = OrdemService().dto_to_model(report_reference_dto.order_service)
                    model.id = report.id_reference
                    if not self._validate_order_closing_contact(model, conn):
                        return {"message": "Cliente de encerramento inválido para a empresa"}, 422
                    if not self._validate_order_technicians(model, id_client, conn):
                        return {"message": "Técnico de encerramento inválido para este tenant"}, 422
                    self.report_repository.create_reference_ordem_service(model, conn)
                    self.report_repository.replace_order_technicians(model.id, model.closing_technician_ids, conn)
                case TypesReport.NEEDS_ASSESSMENT.value:
                    dto = report_reference_dto.needs_assessment
                    if dto is None:
                        return {"message": "Dados do levantamento ausentes"}, 422
                    if not self.needs_repository.validate_relations(dto, id_client, conn):
                        return {"message": "Empresa ou equipamento inválido para este cliente"}, 422
                    saved_needs = self.needs_repository.upsert(report.id_reference, dto, conn)

            result = ApiResult.success_result(
                data={"updated_at": saved_needs["updated_at"].isoformat()} if report.type == TypesReport.NEEDS_ASSESSMENT.value else None,
                message="Reference created successfully",
                status_code=200
            )

            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def update_reference(self, report_reference_dto: ReportReferenceDTO, app_user_id: str, id_client: str):
        conn = get_connection()
        try:

            report = self.report_repository.get_by_id_reference_and_id_client(report_reference_dto.id, id_client, conn)

            if not report:
                return {"message": "Report not found"}, 422

            match report.type:
                case TypesReport.ORDEM_SERVICE.value:
                    if report_reference_dto.order_service is None:
                        return {"message": "Dados da Ordem de Serviço ausentes"}, 422
                    model = OrdemService().dto_to_model(report_reference_dto.order_service)
                    model.id = report.id_reference
                    if not self._validate_order_closing_contact(model, conn):
                        return {"message": "Cliente de encerramento inválido para a empresa"}, 422
                    if not self._validate_order_technicians(model, id_client, conn):
                        return {"message": "Técnico de encerramento inválido para este tenant"}, 422
                    self.report_repository.update_reference_ordem_service(model, conn)
                    self.report_repository.replace_order_technicians(model.id, model.closing_technician_ids, conn)
                case TypesReport.NEEDS_ASSESSMENT.value:
                    dto = report_reference_dto.needs_assessment
                    if dto is None:
                        return {"message": "Dados do levantamento ausentes"}, 422
                    existing = self.needs_repository.get_by_id(report.id_reference, conn, for_update=True)
                    if existing and str(existing["id_company"]) != dto.id_company:
                        return {"message": "A empresa do relatório não pode ser alterada"}, 422
                    if existing and dto.base_updated_at and existing["updated_at"].isoformat() != dto.base_updated_at:
                        return {"message": "Este levantamento foi alterado em outro aparelho. Sincronize antes de reenviar."}, 409
                    if not self.needs_repository.validate_relations(dto, id_client, conn):
                        return {"message": "Empresa ou equipamento inválido para este cliente"}, 422
                    saved_needs = self.needs_repository.upsert(report.id_reference, dto, conn)

            result = ApiResult.success_result(
                data={"updated_at": saved_needs["updated_at"].isoformat()} if report.type == TypesReport.NEEDS_ASSESSMENT.value else None,
                message="Reference updated successfully",
                status_code=200
            )

            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def delete(self, id: str, id_client: str):
        return self.delete_bulk([id], id_client)

    def delete_web(self, ordem_service_id: str, id_client: str):
        conn = get_connection()

        try:
            report = self.report_repository.get_by_id_reference_and_id_client(
                ordem_service_id, id_client, conn
            )

            if not report:
                result = ApiResult.not_found_result("Ordem de serviço não encontrada")
                return result.to_dict(), result.status_code

            if report.type == TypesReport.NEEDS_ASSESSMENT.value:
                result = ApiResult.error_result(
                    "Exclusão de levantamento pelo painel web indisponível.", status_code=409
                )
                return result.to_dict(), result.status_code
            deleted_ordem_services = self.report_repository.delete_ordem_service_by_id(
                ordem_service_id,
                conn
            )

            deleted_reports = self.report_repository.delete_report_by_id(
                report.id,
                conn
            )

            result = ApiResult.success_result(
                data={
                    "deleted_reports": deleted_reports,
                    "deleted_ordem_services": deleted_ordem_services
                },
                message="Report e ordem de serviço deletados com sucesso",
                status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao deletar report/ordem de serviço",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def get_orders(self, id_client: str):
        conn = get_connection()

        rows = self.report_repository.get_orders(conn, id_client)

        result = ApiResult.success_result(
            data=rows,
            message="Company order counts fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def get_dashboard(self, id_client: str):
        conn = get_connection()

        totals = self.report_repository.get_dashboard_totals(conn, id_client)
        last_orders = self.report_repository.get_last_orders(conn, id_client, limit=5)

        orders = [
            {
                "id": row.get("id"),
                "OS_number": row.get("OS_number"),
                "company_name": row.get("company_name"),
                "equipament_name": row.get("equipament_name"),
                "created_at": _format_report_datetime(row.get("created_at")),
            }
            for row in last_orders
        ]

        data = {
            "totals": {
                "companies": int(totals.get("total_companies") or 0),
                "equipaments": int(totals.get("total_equipaments") or 0),
                "reports": int(totals.get("total_reports") or 0),
            },
            "last_orders": orders,
        }

        result = ApiResult.success_result(
            data=data,
            message="Dashboard fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    # def get_ordem_services_by_company(self, company_id: str):
    #     conn = get_connection()

    #     try:
    #         rows = self.report_repository.get_ordem_services_by_company(company_id, conn)

    #         result = ApiResult.success_result(
    #             data=rows,
    #             message="Ordem services fetched successfully",
    #             status_code=200
    #         )

    #         return result.to_dict(), result.status_code
    #     except Exception as e:
    #         result = ApiResult.error_result(
    #             message="Erro ao buscar ordens de serviço da empresa",
    #             status_code=500,
    #             errors=[str(e)]
    #         )
    #         return result.to_dict(), result.status_code
    #     finally:
    #         conn.close()

    def get_ordem_service_by_id(self, ordem_id: str):
        conn = get_connection()

        try:
            row = self.report_repository.get_ordem_service_full_by_id(ordem_id, conn)

            if not row:
                result = ApiResult.not_found_result("Ordem de serviço não encontrada")
                return result.to_dict(), result.status_code

            os_data = {
                k: v
                for k, v in row.items()
                if not k.startswith("company_") and not k.startswith("equipament_")
            }

            os_data = OrdemService.serialize(os_data)

            company_data = {k[len("company_"):]: v for k, v in row.items() if k.startswith("company_")}
            equipament_data = {k[len("equipament_"):]: v for k, v in row.items() if k.startswith("equipament_")}

            company_value = company_data if any(v is not None for v in company_data.values()) else None
            equipament_value = equipament_data if any(v is not None for v in equipament_data.values()) else None

            ordem_service_value = {
                **os_data,
                "company": company_value,
                "equipament": equipament_value
            }

            result = ApiResult.success_result(
                data={"ordem_service": ordem_service_value},
                message="Ordem service fetched successfully",
                status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao buscar ordem de serviço",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def get_ordem_service_by_report_ids(self, id_client: str, report_ids: List[str]):
        conn = get_connection()
        rows = self.report_repository.get_ordem_services_by_report_ids(report_ids, id_client, conn)

        def map_row(row: Dict[str, Any]) -> Dict[str, Any]:
            # Dados principais de ORDEM_SERVICE (exclui colunas de company/equipament e colunas de report)
            os_data = {
                k: v
                for k, v in row.items()
                if not k.startswith("company_")
                and not k.startswith("equipament_")
                and not k.startswith("report_")
                and k != "report_id"
            }

            company_data = {k[len("company_"):]: v for k, v in row.items() if k.startswith("company_")}
            equipament_data = {k[len("equipament_"):]: v for k, v in row.items() if k.startswith("equipament_")}

            company_value = company_data if any(v is not None for v in company_data.values()) else None
            equipament_value = equipament_data if any(v is not None for v in equipament_data.values()) else None

            ordem_service_value = {
                **os_data,
                "company": company_value,
                "equipament": equipament_value
            }

            report_value = {
                "id": row.get("report_id"),
                "type": row.get("report_type"),
                "status": row.get("report_status"),
                "id_client": row.get("report_id_client"),
                "id_app_user": row.get("report_id_app_user"),
                "id_reference": row.get("report_id_reference"),
                "created_at": _format_report_datetime(row.get("report_created_at")),
                "updated_at": _format_report_datetime(row.get("report_updated_at")),
            }

            return {
                "ordem_service": ordem_service_value,
                "report": report_value
            }

        data = [map_row(r) for r in rows]

        result = ApiResult.success_result(
            data=data,
            message="Ordem services fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def delete_bulk(
        self,
        report_ids: List[str],
        id_client: str,
        confirm_media_deletion: bool = False,
    ):
        conn = get_connection()

        try:
            if not report_ids:
                result = ApiResult.validation_error_result(
                    message="Lista de IDs vazia para deleção"
                )
                return result.to_dict(), result.status_code

            owned = self.report_repository.get_owned_report_ids(report_ids, id_client, conn)
            if len(set(owned)) != len(set(report_ids)):
                result = ApiResult.error_result("Um ou mais relatórios não pertencem ao cliente", status_code=403)
                return result.to_dict(), result.status_code

            ordem_service_ids = self.report_repository.get_ordem_service_ids_by_report_ids(
                report_ids=report_ids,
                conn=conn
            )

            needs_ids = self.report_repository.get_report_ids_by_type(
                report_ids, TypesReport.NEEDS_ASSESSMENT.value, conn
            )
            needs_media = self.media_repository.get_manifests(needs_ids, conn)
            media_keys = [
                item["object_key"]
                for manifest in needs_media.values()
                for item in manifest
            ]
            if media_keys and not confirm_media_deletion:
                result = ApiResult.error_result(
                    "Este levantamento possui fotos. Confirme a exclusão para removê-las definitivamente.",
                    status_code=409,
                    data={
                        "requires_media_deletion_confirmation": True,
                        "media_count": len(media_keys),
                    },
                )
                return result.to_dict(), result.status_code

            if media_keys:
                self._delete_bucket_objects(media_keys)

            deleted_ordem_services = self.report_repository.bulk_delete_ordem_service_by_ids(
                ordem_service_ids, conn
            )
            deleted_needs_assessments = self.needs_repository.delete_by_ids(needs_ids, conn)
            deleted_reports = self.report_repository.bulk_delete_reports_by_ids(
                report_ids=report_ids, conn=conn
            )

            result = ApiResult.success_result(
                data={
                    "deleted_reports": deleted_reports,
                    "deleted_ordem_services": deleted_ordem_services,
                    "deleted_needs_assessments": deleted_needs_assessments
                },
                message="Deleção em lote concluída",
                status_code=200
            )

            return result.to_dict(), result.status_code
        except (ClientError, RuntimeError) as e:
            result = ApiResult.error_result(
                message="Não foi possível remover as fotos do storage. Nenhum relatório foi excluído.",
                status_code=502,
                errors=[str(e)],
            )
            return result.to_dict(), result.status_code
        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao deletar reports/ordem_service em lote",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def get_needs_assessment_sync(self, reference_id: str, id_client: str):
        conn = get_connection()
        try:
            report = self.report_repository.get_by_id_reference_and_id_client(
                reference_id, id_client, conn
            )
            if not report or report.type != TypesReport.NEEDS_ASSESSMENT.value:
                result = ApiResult.not_found_result("Levantamento não encontrado")
                return result.to_dict(), result.status_code
            rows = self.needs_repository.get_by_report_ids([report.id], id_client, conn)
            if not rows:
                result = ApiResult.not_found_result("Dados do levantamento não encontrados")
                return result.to_dict(), result.status_code
            row = rows[0]
            needs_data = {
                key: value for key, value in row.items()
                if not key.startswith(("company_", "equipament_")) and key != "report_id"
            }
            company = {key[8:]: value for key, value in row.items() if key.startswith("company_")}
            equipament = {key[11:]: value for key, value in row.items() if key.startswith("equipament_")}
            report_value = report.to_dict()
            for field in ("created_at", "updated_at"):
                report_value[field] = _format_report_datetime(report_value.get(field))
            data = {
                "report": report_value,
                "needs_assessment": {
                    **NeedsAssessment.serialize(needs_data),
                    "company": company,
                    "equipament": equipament if equipament.get("id") else None,
                },
                "media_manifest": self.media_repository.get_manifests([reference_id], conn).get(reference_id, []),
            }
            result = ApiResult.success_result(data=data, message="Levantamento obtido")
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def get_report_sync(self, report_sync_dto: ReportSyncDTO, id_client: str):
        if report_sync_dto.page < 1 or report_sync_dto.limit < 1 or report_sync_dto.limit > 200:
            result = ApiResult.validation_error_result("Paginação inválida")
            return result.to_dict(), result.status_code

        conn = get_connection()
        try:
            total = self.report_repository.get_report_sync_total(id_client, conn)
            page_reports = self.report_repository.get_report_sync_page(
                report_sync_dto.page, report_sync_dto.limit, id_client, conn
            )
            report_ids = [row["id"] for row in page_reports]
            os_rows = {
                row["report_id"]: row
                for row in self.report_repository.get_ordem_services_by_report_ids(
                    report_ids, id_client, conn
                )
            }
            needs_rows = {
                row["report_id"]: row
                for row in self.needs_repository.get_by_report_ids(
                    report_ids, id_client, conn
                )
            }
            manifests = self.media_repository.get_manifests(
                [row["id_reference"] for row in page_reports], conn
            )
            order_technicians = self.report_repository.get_order_technician_ids(
                [row["id"] for row in os_rows.values()], conn
            )
            data = []
            for report in page_reports:
                report_value = dict(report)
                for field in ("created_at", "updated_at"):
                    report_value[field] = _format_report_datetime(report_value.get(field))
                reference_id = report["id_reference"]
                item = {
                    "report": report_value,
                    "media_manifest": manifests.get(reference_id, []),
                }
                if report["type"] == TypesReport.ORDEM_SERVICE.value:
                    row = os_rows.get(report["id"])
                    if not row:
                        data.append(item)
                        continue
                    os_data = {
                        k: v for k, v in row.items()
                        if not k.startswith(("company_", "equipament_", "report_"))
                    }
                    company = {k[8:]: v for k, v in row.items() if k.startswith("company_")}
                    equipament = {k[11:]: v for k, v in row.items() if k.startswith("equipament_")}
                    item["ordem_service"] = {
                        **OrdemService.serialize(os_data),
                        "closing_technician_ids": order_technicians.get(row["id"], []),
                        "company": company if company.get("id") else None,
                        "equipament": equipament if equipament.get("id") else None,
                    }
                elif report["type"] == TypesReport.NEEDS_ASSESSMENT.value:
                    row = needs_rows.get(report["id"])
                    if not row:
                        data.append(item)
                        continue
                    needs_data = {
                        k: v for k, v in row.items()
                        if not k.startswith(("company_", "equipament_")) and k != "report_id"
                    }
                    company = {k[8:]: v for k, v in row.items() if k.startswith("company_")}
                    equipament = {k[11:]: v for k, v in row.items() if k.startswith("equipament_")}
                    item["needs_assessment"] = {
                        **NeedsAssessment.serialize(needs_data),
                        "company": company if company.get("id") else None,
                        "equipament": equipament if equipament.get("id") else None,
                    }
                data.append(item)

            result = ApiResult.success_result(
                data=data,
                message="Reports fetched successfully",
                status_code=200,
                metadata={
                    "total": total,
                    "page_total": math.ceil(total / report_sync_dto.limit),
                    "page": report_sync_dto.page,
                    "limit": report_sync_dto.limit,
                },
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()
