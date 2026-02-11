

from src.dto.api_result import ApiResult
from src.model.ordem_service import OrdemService
from src.enums.types_report import TypesReport
from src.dto.report_reference_dto import ReportReferenceDTO
from src.infra.db import get_connection
from src.dto.report_dto import ReportDTO
from src.enums.status_report import StatusReport
from src.model.report import Report
from src.repository.report_repository import ReportRepository
from typing import Dict, Any, List


class ReportService:

    def __init__(self):
        self.report_repository = ReportRepository()

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

        report = self.report_repository.get_by_id_client_and_id(id, id_client, conn)

        if report is None:
            return ApiResult.error_result(
                message="Report not found",
                status_code=422
            ).to_dict(), 422

        reference = None

        match report.type:
            case TypesReport.ORDEM_SERVICE.value:
                print("ORDEM_SERVICE", report.id_reference)
                reference = self.report_repository.get_reference_ordem_service(report.id_reference, conn)

        result = ApiResult.success_result(
            data=reference,
            message="Reference fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def create(self, report_dto: ReportDTO, app_user_id: str, id_client: str):
        conn = get_connection()

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

    def create_reference(self, report_reference_dto: ReportReferenceDTO, id_client: str):
        conn = get_connection()

        report = self.report_repository.get_by_id_reference_and_id_client(report_reference_dto.id, id_client, conn)

        if not report:
            return {"message": "Report not found"}, 422

        match report.type:
            case TypesReport.ORDEM_SERVICE.value:
                print("ORDEM_SERVICE", report_reference_dto.order_service)
                model = OrdemService().dto_to_model(report_reference_dto.order_service)

                model.id = report.id_reference

                self.report_repository.create_reference_ordem_service(model, conn)

        result = ApiResult.success_result(
            data=None,
            message="Reference created successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def update_reference(self, report_reference_dto: ReportReferenceDTO, app_user_id: str, id_client: str):
        conn = get_connection()

        report = self.report_repository.get_by_id_reference_and_id_client(report_reference_dto.id, id_client, conn)

        if not report:
            return {"message": "Report not found"}, 422
            
        match report.type:
            case TypesReport.ORDEM_SERVICE.value:

                model = OrdemService().dto_to_model(report_reference_dto.order_service)

                model.id = report.id_reference

                self.report_repository.update_reference_ordem_service(model, conn)

        result = ApiResult.success_result(
            data=None,
            message="Reference updated successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def delete(self, id: str, app_user_id: str):
        [], 200

    def get_ordem_service_by_report_ids(self, id_client: str, report_ids: List[str]):
        conn = get_connection()
        rows = self.report_repository.get_ordem_services_by_report_ids(report_ids, id_client, conn)

        def map_row(row: Dict[str, Any]) -> Dict[str, Any]:
            os_data = {k: v for k, v in row.items() if not k.startswith("company_") and not k.startswith("equipament_") and k != "report_id"}
            
            company_data = {k[len("company_"):]: v for k, v in row.items() if k.startswith("company_")}
            equipament_data = {k[len("equipament_"):]: v for k, v in row.items() if k.startswith("equipament_")}

            company_value = company_data if any(v is not None for v in company_data.values()) else None
            equipament_value = equipament_data if any(v is not None for v in equipament_data.values()) else None

            return {
                **os_data,
                "company": company_value,
                "equipament": equipament_value
            }

        data = [map_row(r) for r in rows]

        result = ApiResult.success_result(
            data=data,
            message="Ordem services fetched successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code
