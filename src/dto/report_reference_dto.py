

from typing import Optional
from pydantic import BaseModel
from src.dto.ordem_service_dto import OrdemServiceDTO


class ReportReferenceDTO(BaseModel):
    id: str
    order_service: Optional[OrdemServiceDTO] = None

    