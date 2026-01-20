from datetime import datetime
import uuid
import json
from typing import Optional

from src.dto.client_dto import ClientDTO


class Client:
    def __init__(
        self,
        id: Optional[str] = None,
        document: Optional[str] = None,
        street: Optional[str] = None,
        number: Optional[str] = None,
        complement: Optional[str] = None,
        neighborhood: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        plan: Optional[str] = None,
        plan_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id if id else str(uuid.uuid4())
        self.document = document
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.email = email
        self.plan = plan
        self.plan_id = plan_id
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "document": self.document,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone": self.phone,
            "email": self.email,
            "plan": self.plan,
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def dto_to_model(self, dto: ClientDTO):
        for key, value in dto.model_dump(exclude_unset=True).items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

