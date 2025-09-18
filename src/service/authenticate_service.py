import datetime
from src.service.jwt_service import JwtService
from src.dto.login_dto import LoginDTO
from src.model.app_user import AppUser
from src.repository.app_user_repository import AppUserRepository
from src.dto.app_user_dto import AppUserDTO
from src.infra.db import get_connection
import bcrypt


class AuthenticateService:
    def __init__(self):
        self.user_repo = AppUserRepository()

    def login(self, login_dto: LoginDTO):
        conn = get_connection()

        try:
            user: AppUser = self.user_repo.find_by_email(login_dto.email, conn)

            if not user:
                return {"message": "User not found"}, 404

            if not bcrypt.checkpw(login_dto.password.encode('utf-8'), user.password.encode('utf-8')):
                return {"message": "Invalid password"}, 401

            jwt_service = JwtService()

            token = jwt_service.generate_token({
                "user_id": user.id,
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            })

            return {"message": "Login successful", "token": token}, 200
        except Exception as e:
            raise e
        finally:
            conn.close()

    def register(self, user_dto: AppUserDTO):
        conn = get_connection()

        try:
            hashed = bcrypt.hashpw(user_dto.password.encode('utf-8'), bcrypt.gensalt())

            user = AppUser(email=user_dto.email, password=hashed.decode('utf-8'), name=user_dto.name,
                           document=user_dto.document, id_client=user_dto.id_client)

            user = self.user_repo.create(user, conn)

            conn.commit()

            return {"message": "User created successfully"}, 201

        except Exception as e:
            raise e

        finally:
            conn.close()
