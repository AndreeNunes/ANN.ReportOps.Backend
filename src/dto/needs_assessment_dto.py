from typing import Optional

from pydantic import BaseModel, Field


class NeedsAssessmentDTO(BaseModel):
    base_updated_at: Optional[str] = None
    id_company: str = Field(min_length=1, max_length=36)
    id_equipament: Optional[str] = Field(default=None, max_length=36)
    external_compressor_notes: Optional[str] = None
    internal_compressor_notes: Optional[str] = None
    air_filter: Optional[bool] = None
    oil_filter: Optional[bool] = None
    air_oil_separator: Optional[bool] = None
    pre_coalescing: Optional[bool] = None
    post_coalescing: Optional[bool] = None
    belts: Optional[bool] = None
    hoses: Optional[bool] = None
