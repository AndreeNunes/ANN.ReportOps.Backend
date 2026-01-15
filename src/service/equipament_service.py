from src.dto.api_result import ApiResult
from src.model.equipament import Equipament
from src.dto.equipament_dto import EquipamentDTO
from src.repository.equipament_repository import EquipamentRepository
from src.infra.db import get_connection



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
                status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

    def create(self, equipament_dto: EquipamentDTO, company_id: str):
        conn = get_connection()

        try:
            equipament: Equipament = Equipament().dto_to_model(equipament_dto)
            equipament.company_id = company_id
            self.equipament_repo.add(equipament, conn)
            conn.commit()

            result = ApiResult.success_result(
                data=None,
                message="Equipamento criado com sucesso",
                status_code=200
            )

            return result.to_dict(), result.status_code
        except Exception as e:
            raise e
        finally:
            conn.close()

        return self.equipament_repo.add(equipament)