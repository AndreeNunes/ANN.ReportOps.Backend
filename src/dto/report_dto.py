from pydantic import BaseModel

from src.enums.types_report import TypesReport


class ReportDTO(BaseModel):
    type: TypesReport
