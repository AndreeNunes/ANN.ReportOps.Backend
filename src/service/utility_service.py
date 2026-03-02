import requests
from src.dto.api_result import ApiResult

BRASIL_API_CEP_URL = "https://brasilapi.com.br/api/cep/v2"


class UtilityService:
    def get_address_by_cep(self, cep: str):
        try:
            response = requests.get(f"{BRASIL_API_CEP_URL}/{cep}", timeout=10)

            if response.status_code == 404:
                result = ApiResult.not_found_result("CEP não encontrado")
                return result.to_dict(), result.status_code

            if response.status_code != 200:
                result = ApiResult.error_result(
                    message="Erro ao consultar CEP",
                    status_code=response.status_code
                )
                return result.to_dict(), result.status_code

            data = response.json()

            address = {
                "cep": data.get("cep"),
                "street": data.get("street"),
                "neighborhood": data.get("neighborhood"),
                "city": data.get("city"),
                "state": data.get("state"),
            }

            result = ApiResult.success_result(
                data=address,
                message="CEP encontrado com sucesso"
            )

            return result.to_dict(), result.status_code

        except requests.exceptions.Timeout:
            result = ApiResult.error_result(
                message="Timeout ao consultar CEP",
                status_code=504
            )
            return result.to_dict(), result.status_code
        except Exception as e:
            result = ApiResult.error_result(
                message="Erro ao consultar CEP",
                status_code=500,
                errors=[str(e)]
            )
            return result.to_dict(), result.status_code
