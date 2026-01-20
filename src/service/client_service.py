import bcrypt
import secrets
import string
from datetime import datetime
from src.dto.api_result import ApiResult
from src.dto.client_dto import ClientDTO, ClientCodeValidationDTO
from src.infra.db import get_connection
from src.model.client import Client
from src.model.plan import Plan
from src.repository.client_repository import ClientRepository
from src.repository.plan_repository import PlanRepository


class ClientService:
    def __init__(self):
        self.client_repo = ClientRepository()
        self.plan_repo = PlanRepository()

    def create(self, client_dto: ClientDTO):
        conn = get_connection()
        try:
            # Gera código de acesso em texto claro e hash
            alphabet = string.ascii_uppercase + string.digits
            access_code = "".join(secrets.choice(alphabet) for _ in range(6))
            hashed = bcrypt.hashpw(access_code.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            plan = Plan(
                access_validate=hashed,
                access_date_valid=client_dto.access_date_valid if client_dto.access_date_valid else datetime.now()
            )
            self.plan_repo.create(plan, conn)

            client = Client().dto_to_model(client_dto)
            client.plan_id = plan.id
            self.client_repo.create(client, conn)

            conn.commit()

            result = ApiResult.success_result(
                data=client.to_dict(),
                message="Cliente criado com sucesso",
                status_code=201,
                metadata={"access_code": access_code, "plan_id": plan.id}
            )
            return result.to_dict(), result.status_code
        except Exception as e:
            conn.rollback()
            result = ApiResult.error_result(
                message="Erro ao criar cliente",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def validate_code(self, payload: ClientCodeValidationDTO):
        conn = get_connection()
        try:
            valid_plans = self.plan_repo.get_all_valid(conn)
            matched_plan = None
            for plan in valid_plans:
                if bcrypt.checkpw(payload.code.encode("utf-8"), plan["access_validate"].encode("utf-8")):
                    matched_plan = plan
                    break

            if not matched_plan:
                result = ApiResult.validation_error_result("Código inválido ou expirado")
                return result.to_dict(), result.status_code

            client = self.client_repo.get_by_plan_id(matched_plan["id"], conn)
            if not client:
                result = ApiResult.not_found_result("Cliente não encontrado")
                return result.to_dict(), result.status_code

            result = ApiResult.success_result(
                data={"client_id": client["id"], "plan_id": matched_plan["id"]},
                message="Código válido",
                status_code=200
            )
            return result.to_dict(), result.status_code
        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao validar código",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

