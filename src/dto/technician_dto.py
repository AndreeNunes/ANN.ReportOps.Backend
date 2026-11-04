from typing import Optional
from pydantic import BaseModel, Field

class TechnicianDTO(BaseModel):
    id: Optional[str] = Field(default=None, min_length=1, max_length=36)
    name: str = Field(min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=50)

class TechnicianSignatureDTO(BaseModel):
    content_type: str = Field(pattern=r"^image/png$")
    size_bytes: int = Field(ge=1, le=20 * 1024 * 1024)

class TechnicianSignatureCompleteDTO(TechnicianSignatureDTO):
    object_key: str = Field(min_length=1, max_length=512)
