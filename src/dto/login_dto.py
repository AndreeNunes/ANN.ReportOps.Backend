from pydantic import BaseModel, EmailStr, constr


class LoginDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
