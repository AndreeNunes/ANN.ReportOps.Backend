import json
import uuid


class Report:
    def __init__(self, type: str, status: str, id_app_user: str):
        self.id = uuid.uuid4()
        self.type = type
        self.status = status
        self.id_app_user = id_app_user
        self.reference_id = uuid.uuid4()

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "id_app_user": self.id_app_user,
            "reference_id": self.reference_id
        }
