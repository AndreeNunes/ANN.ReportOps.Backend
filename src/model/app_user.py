class AppUser:
    def __init__(self, id=None, email=None, password=None, name=None, document=None, client_id=None, created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.document = document
        self.client_id = client_id
        self.created_at = created_at
        self.updated_at = updated_at
