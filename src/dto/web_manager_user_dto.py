from pydantic import BaseModel, EmailStr, constr


class WebManagerUserDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    name: constr(min_length=2, max_length=100)
    id_client: constr(min_length=1)

