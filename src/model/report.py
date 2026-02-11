from datetime import datetime
import json
import uuid


class Report:
    def __init__(self, id: str = None, type: str = None, status: str = None, id_client: str = None, id_app_user: str = None, id_reference: str = None, created_at: str = None, updated_at: str = None):
        self.id = id if id else str(uuid.uuid4())
        self.type = type
        self.status = status
        self.id_client = id_client
        self.id_app_user = id_app_user
        self.id_reference = id_reference if id_reference else str(uuid.uuid4())
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "id_client": self.id_client,
            "id_app_user": self.id_app_user,
            "id_reference": self.id_reference,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
