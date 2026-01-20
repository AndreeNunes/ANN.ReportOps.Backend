from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClientDTO(BaseModel):
    document: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    plan: Optional[str] = None
    access_date_valid: Optional[datetime] = None


class ClientCodeValidationDTO(BaseModel):
    code: str

