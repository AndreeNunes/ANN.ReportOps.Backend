

import uuid
from src.dto.api_result import ApiResult
from src.dto.company_dto import CompanyDTO
from src.infra.db import get_connection
from src.model.company import Company
from src.repository.company_repository import CompanyRepository


class CompanyService:
    def __init__(self):
        self.company_repo = CompanyRepository()

    def get_all(self, id_client: str):
        conn = get_connection()

        try:
            companies_data = self.company_repo.get_all(conn, id_client)

            result = ApiResult.success_result(
                data=companies_data,
                message=f"Encontradas {len(companies_data)} empresas",
                metadata={"total_count": len(companies_data), "id_client": id_client}
            )

            return result.to_dict(), result.status_code

        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao buscar empresas",
                status_code=500,
                errors=[str(e)]
            )
            
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def create(self, company_dto: CompanyDTO, id_client: str):
        conn = get_connection()

        try:
            company = Company(
                id=str(uuid.uuid4()),
                name=company_dto.name,
                document=company_dto.document,
                street=company_dto.street,
                number=company_dto.number,
                complement=company_dto.complement,
                neighborhood=company_dto.neighborhood,
                city=company_dto.city,
                state=company_dto.state,
                zip_code=company_dto.zip_code,
                phone=company_dto.phone,
                email=company_dto.email,
                id_client=id_client
            )

            self.company_repo.create(company, conn)

            result = ApiResult.success_result(
                data=company.to_dict(),
                message="Empresa criada com sucesso",
                status_code=201
            )

            return result.to_dict(), result.status_code

        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao criar empresa",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()

    def delete(self, id: str, id_client: str):
        conn = get_connection()

        try:
            company = self.company_repo.get_by_id(id, conn)

            if not company:
                result = ApiResult.not_found_result("Empresa não encontrada")
                return result.to_dict(), result.status_code

            self.company_repo.delete(id, conn)

            result = ApiResult.success_result(
                data=None,
                message="Empresa deletada com sucesso",
                status_code=200
            )

            return result.to_dict(), result.status_code

        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao deletar empresa",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
        finally:
            conn.close()
