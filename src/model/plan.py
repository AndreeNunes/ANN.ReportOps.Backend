from datetime import datetime
import uuid


class Plan:
    def __init__(self, id: str = None, access_validate: str = None, access_date_valid: datetime = None):
        self.id = id if id else str(uuid.uuid4())
        self.access_validate = access_validate
        self.access_date_valid = access_date_valid if access_date_valid else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "access_validate": self.access_validate,
            "access_date_valid": self.access_date_valid
        }

