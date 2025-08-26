from typing import Any, Optional, Dict
from dataclasses import dataclass


@dataclass
class ApiResult:
    """
    Classe para padronizar respostas da API
    """
    data: Any
    status_code: int = 200
    message: str = "Sucesso"
    success: bool = True
    errors: Optional[list] = None
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """
        Converte o resultado para dicionário
        """
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
                       status_code: int = 200, metadata: Optional[Dict] = None) -> 'ApiResult':
        """
        Cria um resultado de sucesso
        """
        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success=True,
            metadata=metadata
        )

    @classmethod
    def error_result(cls, message: str = "Erro na operação", status_code: int = 400,
                     errors: Optional[list] = None, data: Any = None) -> 'ApiResult':
        """
        Cria um resultado de erro
        """
        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success=False,
            errors=errors or []
        )

    @classmethod
    def not_found_result(cls, message: str = "Recurso não encontrado",
                         data: Any = None) -> 'ApiResult':
        """
        Cria um resultado para recurso não encontrado
        """
        return cls.error_result(
            message=message,
            status_code=404,
            data=data
        )

    @classmethod
    def validation_error_result(cls, message: str = "Dados inválidos",
                                errors: Optional[list] = None) -> 'ApiResult':
        return cls.error_result(
            message=message,
            status_code=422,
            errors=errors
        )
