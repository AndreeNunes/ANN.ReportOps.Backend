import uuid
import bcrypt
from src.dto.login_dto import LoginDTO
from src.dto.web_manager_user_dto import WebManagerUserDTO
from src.model.web_manager_user import WebManagerUser
from src.repository.web_manager_user_repository import WebManagerUserRepository
from src.service.jwt_service import JwtService
from src.infra.db import get_connection


class WebAuthenticateService:
    def __init__(self):
        self.user_repo = WebManagerUserRepository()

    def login(self, login_dto: LoginDTO):
        conn = get_connection()

        try:
            user = self.user_repo.find_by_email(login_dto.email, conn)

            if not user:
                return {"message": "User not found"}, 404

            if not bcrypt.checkpw(login_dto.password.encode('utf-8'), user.password.encode('utf-8')):
                return {"message": "Invalid password"}, 401

            jwt_service = JwtService()
            token = jwt_service.generate_token({
                "name": user.name,
                "web_user_id": user.id,
                "email": user.email,
                "client_id": user.id_client
            })

            return {"message": "Login successful", "token": token}, 200
        except Exception as e:
            raise e
        finally:
            conn.close()

    def register(self, user_dto: WebManagerUserDTO):
        conn = get_connection()

        try:
            existing = self.user_repo.find_by_email(user_dto.email, conn)
            if existing:
                return {"message": "E-mail já cadastrado"}, 409

            hashed = bcrypt.hashpw(user_dto.password.encode('utf-8'), bcrypt.gensalt())

            user = WebManagerUser(
                id=str(uuid.uuid4()),
                name=user_dto.name,
                email=user_dto.email,
                password=hashed.decode('utf-8'),
                id_client=user_dto.id_client
            )

            self.user_repo.create(user, conn)
            conn.commit()

            return {"message": "User created successfully"}, 201
        except Exception as e:
            raise e
        finally:
            conn.close()

