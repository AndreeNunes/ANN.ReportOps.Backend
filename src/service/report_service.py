

from dto.report_dto import ReportDTO
from enums.status_report import StatusReport
from src.model.report import Report


class ReportService:

    def get_all(self, app_user_id: str):
        return [], 200

    def create(self, report_dto: ReportDTO, app_user_id: str):

        report = Report(
            type=report_dto.type,
            status=StatusReport.IN_PROGRESS,
            id_app_user=app_user_id
        )

        return report.to_dict(), 200

    def delete(self, id: str, app_user_id: str):
        [], 200
