class AppUser:
    def __init__(self, id=None, email=None, password=None, name=None, document=None, id_client=None, created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.document = document
        self.id_client = id_client
        self.created_at = created_at
        self.updated_at = updated_at
