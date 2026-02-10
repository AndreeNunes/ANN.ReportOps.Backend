from typing import Any, Dict, Optional
from src.repository.app_user_repository import AppUserRepository
from src.repository.client_repository import ClientRepository
from src.infra.db import get_connection
from src.model.app_user import AppUser


class ProfileService:
    def __init__(self):
        self.user_repo = AppUserRepository()
        self.client_repo = ClientRepository()

    def get_profile(self, app_user_id: str):
        if not app_user_id:
            return {"message": "App-User-Id header obrigatório"}, 400

        conn = get_connection()
        try:
            user: Optional[AppUser] = self.user_repo.find_by_id(app_user_id, conn)
            if not user:
                return {"message": "Usuário não encontrado"}, 404

            client: Optional[Dict[str, Any]] = None
            if user.id_client:
                client = self.client_repo.get_by_id(user.id_client, conn)

            user_payload = {
                "name": user.name,
                "email": user.email,
                "document": user.document
            }

            company_payload = None
            if client:
                address_parts = [
                    client.get("street"),
                    client.get("number"),
                    client.get("complement"),
                    client.get("neighborhood"),
                    client.get("city"),
                    client.get("state"),
                    client.get("zip_code"),
                ]
                # Filtra None/strings vazias e junta por ", "
                address = ", ".join([str(p) for p in address_parts if p])

                company_payload = {
                    "document": client.get("document"),
                    "name": client.get("name"),
                    "address": address,
                    "phone": client.get("phone"),
                    "email": client.get("email")
                }

            return {
                "user": user_payload,
                "company": company_payload
            }, 200
        except Exception as e:
            raise e
        finally:
            conn.close()

