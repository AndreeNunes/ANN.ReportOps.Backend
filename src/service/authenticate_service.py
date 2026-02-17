import datetime
from src.service.jwt_service import JwtService
from src.dto.login_dto import LoginDTO
from src.model.app_user import AppUser
from src.repository.app_user_repository import AppUserRepository
from src.dto.app_user_dto import AppUserDTO
from src.infra.db import get_connection
import bcrypt
from src.dto.client_dto import ClientCodeValidationDTO
from src.repository.plan_repository import PlanRepository
from src.repository.client_repository import ClientRepository


class AuthenticateService:
    def __init__(self):
        self.user_repo = AppUserRepository()
        self.plan_repo = PlanRepository()
        self.client_repo = ClientRepository()

    def login(self, login_dto: LoginDTO):
        conn = get_connection()

        try:
            user: AppUser = self.user_repo.find_by_email(login_dto.email, conn)

            if not user:
                return {"message": "User not found"}, 404

            if not bcrypt.checkpw(login_dto.password.encode('utf-8'), user.password.encode('utf-8')):
                return {"message": "Invalid password"}, 401

            # Busca data de validade do plano do cliente
            plan_access_date_valid_iso = None
            try:
                client = self.client_repo.get_by_id(user.id_client, conn) if user.id_client else None
                if client and client.get("plan_id"):
                    plan = self.plan_repo.get_by_id(client["plan_id"], conn)
                    if plan and plan.get("access_date_valid"):
                        plan_access_date_valid_iso = plan["access_date_valid"].isoformat()
            except Exception:
                # Não falhar o login por erro ao coletar metadados do plano
                plan_access_date_valid_iso = None

            jwt_service = JwtService()

            token = jwt_service.generate_token({
                "name": user.name,
                "app_user_id": user.id,
                "email": user.email,
                "client_id": user.id_client,
                "plan_access_date_valid": plan_access_date_valid_iso
            })

            return {"message": "Login successful", "token": token}, 200
        except Exception as e:
            raise e
        finally:
            conn.close()

    def register(self, user_dto: AppUserDTO):
        conn = get_connection()

        try:
            derived_client_id = None

            if user_dto.code:
                valid_plans = self.plan_repo.get_all_valid(conn)

                matched_plan = None

                for plan in valid_plans:
                    if bcrypt.checkpw(user_dto.code.encode('utf-8'), plan["access_validate"].encode('utf-8')):
                        matched_plan = plan
                        break

                if not matched_plan:
                    return {"message": "Código inválido ou expirado"}, 422

                client = self.client_repo.get_by_plan_id(matched_plan["id"], conn)
                if not client:
                    return {"message": "Cliente não encontrado para o código informado"}, 404

                derived_client_id = client["id"]
            else:
                if not user_dto.id_client:
                    return {"message": "id_client ou code é obrigatório"}, 422
                    
                derived_client_id = user_dto.id_client

            hashed = bcrypt.hashpw(user_dto.password.encode('utf-8'), bcrypt.gensalt())

            user = AppUser(email=user_dto.email, password=hashed.decode('utf-8'), name=user_dto.name,
                           document=user_dto.document, id_client=derived_client_id)

            user = self.user_repo.create(user, conn)

            conn.commit()

            return {"message": "User created successfully"}, 201

        except Exception as e:
            raise e

        finally:
            conn.close()

    def validate_user_code(self, payload: ClientCodeValidationDTO):
        conn = get_connection()
        try:
            valid_plans = self.plan_repo.get_all_valid(conn)
            matched_plan = None
            for plan in valid_plans:
                if bcrypt.checkpw(payload.code.encode('utf-8'), plan["access_validate"].encode('utf-8')):
                    matched_plan = plan
                    break

            if not matched_plan:
                return {"message": "Código inválido ou expirado"}, 422

            client = self.client_repo.get_by_plan_id(matched_plan["id"], conn)
            if not client:
                return {"message": "Cliente não encontrado para o código informado"}, 404

            return {
                "message": "Código válido",
                "client_id": client["id"],
                "plan_id": matched_plan["id"]
            }, 200
        except Exception as e:
            raise e
        finally:
            conn.close()
