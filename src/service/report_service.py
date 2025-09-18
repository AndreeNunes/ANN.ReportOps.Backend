

from src.dto.api_result import ApiResult
from src.model.ordem_service import OrdemService
from src.enums.types_report import TypesReport
from src.dto.report_reference_dto import ReportReferenceDTO
from src.infra.db import get_connection
from src.dto.report_dto import ReportDTO
from src.enums.status_report import StatusReport
from src.model.report import Report
from src.repository.report_repository import ReportRepository


class ReportService:

    def __init__(self):
        self.report_repository = ReportRepository()

    def get_all(self, app_user_id: str):
        
        return [], 200

    def create(self, report_dto: ReportDTO, app_user_id: str):
        conn = get_connection()
        
        report = Report(
            type=report_dto.type.value,
            status=StatusReport.IN_PROGRESS.value,
            id_app_user=app_user_id
        )

        report = self.report_repository.create(report, conn)

        return report.to_dict(), 200

    def create_reference(self, report_reference_dto: ReportReferenceDTO, app_user_id: str):
        conn = get_connection()

        report = self.report_repository.get_by_id_and_app_user_id(report_reference_dto.id, app_user_id, conn)

        if not report:
            return {"message": "Report not found"}, 422

        match report.type:
            case TypesReport.ORDEM_SERVICE.value:
                model = OrdemService().dto_to_model(report_reference_dto.order_service)

                model.id = report.id_reference

                self.report_repository.create_reference_ordem_service(model, conn)

        result = ApiResult.success_result(
            data=None,
            message="Reference created successfully",
            status_code=200
        )

        return result.to_dict(), result.status_code

    def delete(self, id: str, app_user_id: str):
        [], 200
