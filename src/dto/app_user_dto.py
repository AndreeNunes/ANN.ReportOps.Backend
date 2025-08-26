from pydantic import BaseModel, EmailStr, constr


class AppUserDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    name: constr(min_length=2, max_length=100)
    document: constr(min_length=5, max_length=30)
    client_id: str
