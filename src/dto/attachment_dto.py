from typing import Literal, Optional

from pydantic import BaseModel, Field


MediaType = Literal["photo", "signature"]


class MediaUploadItemDTO(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    type: MediaType
    content_type: Literal["image/jpeg", "image/png"]
    size_bytes: int = Field(ge=1, le=20 * 1024 * 1024)
    note: Optional[str] = Field(default=None, max_length=2000)
    group: Optional[str] = Field(default=None, max_length=64)


class MediaUploadRequestDTO(BaseModel):
    media: list[MediaUploadItemDTO] = Field(default_factory=list, max_length=30)


class MediaFinalizeItemDTO(MediaUploadItemDTO):
    object_key: str = Field(min_length=1, max_length=512)


class MediaVersionDTO(BaseModel):
    id: str
    object_key: str
    updated_at: str


class MediaFinalizeRequestDTO(BaseModel):
    media: list[MediaFinalizeItemDTO] = Field(default_factory=list, max_length=500)
    base_media: Optional[list[MediaVersionDTO]] = Field(default=None, max_length=500)
