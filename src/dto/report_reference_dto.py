

from typing import Optional
from pydantic import BaseModel
from src.dto.ordem_service_dto import OrdemServiceDTO
from src.dto.needs_assessment_dto import NeedsAssessmentDTO


class ReportReferenceDTO(BaseModel):
    id: str
    order_service: Optional[OrdemServiceDTO] = None
    needs_assessment: Optional[NeedsAssessmentDTO] = None

    