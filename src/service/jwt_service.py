import os
import jwt
import datetime


class JwtService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = "HS256"
        self.expires_hours = 168

    def generate_token(self, payload: dict):
        payload = payload.copy()
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=self.expires_hours)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
