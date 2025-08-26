from http import HTTPStatus
from typing import Any, Optional, Dict
from dataclasses import dataclass


@dataclass
class ApiResult:
    """
    Classe para padronizar respostas da API
    """
    data: Any
    status_code: HTTPStatus = HTTPStatus.OK
    message: str = "Sucesso"
    success: bool = True
    errors: Optional[list] = None
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        result = {
            "success": self.success,
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data
        }

        if self.errors:
            result["errors"] = self.errors

        if self.metadata:
            result["metadata"] = self.metadata

        return result

    @classmethod
    def success_result(cls, data: Any, message: str = "Operação realizada com sucesso",
                       status_code: HTTPStatus = HTTPStatus.OK, metadata: Optional[Dict] = None) -> 'ApiResult':
        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success=True,
            metadata=metadata
        ), status_code

    @classmethod
    def error_result(cls, message: str = "Erro na operação", status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
                     errors: Optional[list] = None, data: Any = None) -> 'ApiResult':

        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success=False,
            errors=errors or []
        ), status_code

    @classmethod
    def not_found_result(cls, message: str = "Recurso não encontrado",
                         data: Any = None) -> 'ApiResult':

        return cls.error_result(
            message=message,
            status_code=HTTPStatus.NOT_FOUND,
            data=data
        ), HTTPStatus.NOT_FOUND
