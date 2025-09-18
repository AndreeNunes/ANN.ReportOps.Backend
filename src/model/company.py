import json


class Company:

    def __init__(self, id: str, name: str, document: str, street: str, number: str, complement: str, neighborhood: str, city: str, state: str, zip_code: str, phone: str, email: str, id_client: str, created_at: str = None, updated_at: str = None):
        self.id = id
        self.name = name
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
        self.id_client = id_client
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
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
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "id_client": self.id_client
        }

    def to_json(self):
        return json.dumps(self.to_dict())
