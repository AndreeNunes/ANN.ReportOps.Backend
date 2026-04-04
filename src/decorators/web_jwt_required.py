from functools import wraps

from flask import g, request

from src.dto.api_result import ApiResult
from src.service.jwt_service import JwtService


def web_jwt_required(f):
    """
    Exige Authorization: Bearer <token> emitido no login web.
    Disponibiliza em g.web_jwt_payload o payload decodificado e g.web_client_id.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            r = ApiResult.error_result(
                message="Token não informado",
                status_code=401,
            )
            return r.to_dict(), r.status_code

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            r = ApiResult.error_result(
                message="Token inválido",
                status_code=401,
            )
            return r.to_dict(), r.status_code

        payload = JwtService().decode_token(token)
        
        if payload is None:
            r = ApiResult.error_result(
                message="Token inválido ou expirado",
                status_code=401,
            )
            return r.to_dict(), r.status_code

        client_id = payload.get("client_id")
        if not client_id:
            r = ApiResult.error_result(
                message="Token de acesso web inválido",
                status_code=403,
            )
            return r.to_dict(), r.status_code

        g.web_jwt_payload = payload
        g.web_client_id = client_id
        return f(*args, **kwargs)

    return decorated
