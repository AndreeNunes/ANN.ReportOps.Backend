from typing import Optional
from pydantic import BaseModel

from src.enums.types_report import TypesReport


class ReportDTO(BaseModel):
    id: Optional[str] = None
    id_reference: Optional[str] = None
    type: TypesReport
