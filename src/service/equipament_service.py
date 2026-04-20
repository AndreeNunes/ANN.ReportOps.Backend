from datetime import datetime

from src.dto.api_result import ApiResult
from src.dto.equipament_dto import EquipamentDTO
from src.infra.db import get_connection
from src.model.equipament import Equipament
from src.repository.equipament_repository import EquipamentRepository


class EquipamentService:
    def __init__(self):
        self.equipament_repo = EquipamentRepository()

    def get_all(self, company_id: str):
        conn = get_connection()

        try:
            equipament = self.equipament_repo.get_all(conn, company_id)

            result = ApiResult.success_result(
                data=equipament,
                message="Equipamentos encontrados com sucesso",
                status_code=200,
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

    def get_all_by_client(self, client_id: str):
        conn = get_connection()

        try:
            equipaments = self.equipament_repo.get_all_by_client(conn, client_id)

            result = ApiResult.success_result(
                data=equipaments,
                message="Equipamentos encontrados com sucesso",
                status_code=200,
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

    def create(self, equipament_dto: EquipamentDTO, company_id: str):
        conn = get_connection()

        try:
            print("Criando equipamento com dados:", equipament_dto)
            
            equipament: Equipament = Equipament().dto_to_model(equipament_dto)
            equipament.company_id = company_id
            self.equipament_repo.add(equipament, conn)
            conn.commit()

            result = ApiResult.success_result(
                data=None, message="Equipamento criado com sucesso", status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

        return self.equipament_repo.add(equipament)

    def update(self, equipament_dto: EquipamentDTO, company_id: str):
        if not equipament_dto.id:
            result = ApiResult.validation_error_result(
                message="Id do equipamento é obrigatório para atualização"
            )
            return result.to_dict(), result.status_code

        conn = get_connection()

        try:
            current = self.equipament_repo.get_by_id(
                conn, equipament_dto.id, company_id
            )

            if not current:
                result = ApiResult.not_found_result("Equipamento não encontrado")
                return result.to_dict(), result.status_code

            equipament = Equipament()
            equipament.id = current["id"]
            equipament.company_id = current["company_id"]
            equipament.dto_to_model(equipament_dto)
            equipament.updated_at = datetime.now()

            self.equipament_repo.update(equipament, conn)

            result = ApiResult.success_result(
                data=None, message="Equipamento atualizado com sucesso", status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

    def delete(self, id: str, company_id: str):
        conn = get_connection()

        try:
            current = self.equipament_repo.get_by_id(conn, id, company_id)

            if not current:
                result = ApiResult.not_found_result("Equipamento não encontrado")
                return result.to_dict(), result.status_code

            self.equipament_repo.delete(conn, id, company_id)

            result = ApiResult.success_result(
                data=None, message="Equipamento deletado com sucesso", status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

    def get_by_id_with_out_company(self, id: str):
        conn = get_connection()
        
        try:
            equipament = self.equipament_repo.get_by_id_with_out_company(conn, id)

            if not equipament:
                result = ApiResult.not_found_result("Equipamento não encontrado")
                return result.to_dict(), result.status_code

            result = ApiResult.success_result(
                data=equipament,
                message="Equipamento encontrado com sucesso",
                status_code=200,
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()
