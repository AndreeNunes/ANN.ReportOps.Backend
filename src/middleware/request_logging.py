import json
import time
import uuid
import logging

from flask import request, g

logger = logging.getLogger("reportops")

# Cabecalhos sensiveis: o valor e mascarado (nunca logamos o token).
SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "proxy-authorization",
}

# Chaves sensiveis dentro do body/query: o valor e mascarado.
SENSITIVE_KEYS = {
    "password",
    "senha",
    "token",
    "secret",
    "access_token",
    "refresh_token",
}

MAX_BODY_CHARS = 4000  # corta bodies muito grandes


def _safe_headers(headers):
    return {
        k: ("***" if k.lower() in SENSITIVE_HEADERS else v)
        for k, v in headers.items()
    }


def _redact(obj):
    if isinstance(obj, dict):
        return {
            k: ("***" if k.lower() in SENSITIVE_KEYS else _redact(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_redact(i) for i in obj]
    return obj


def _safe_body():
    """Extrai o body de forma segura, sem ler arquivos binarios de upload."""
    if request.method in ("GET", "HEAD", "DELETE"):
        return None

    content_type = request.content_type or ""

    if "multipart/form-data" in content_type:
        # Upload de arquivo: registra apenas os nomes dos campos, nunca o binario.
        return {
            "_files": list(request.files.keys()),
            "_form": _redact(request.form.to_dict()),
        }

    if "application/json" in content_type:
        data = request.get_json(silent=True)
        return _redact(data) if data is not None else None

    if "application/x-www-form-urlencoded" in content_type:
        return _redact(request.form.to_dict())

    raw = request.get_data(cache=True, as_text=True)
    return raw[:MAX_BODY_CHARS] if raw else None


def register_request_logging(app):
    """Registra os hooks que logam toda requisicao recebida."""

    @app.before_request
    def _start_timer():
        g._req_start = time.perf_counter()
        g._req_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex

    @app.after_request
    def _log_request(response):
        try:
            start = getattr(g, "_req_start", time.perf_counter())
            entry = {
                "request_id": getattr(g, "_req_id", None),
                "method": request.method,
                "path": request.path,
                "url": request.url,
                "query": _redact(request.args.to_dict()),
                "headers": _safe_headers(request.headers),
                "body": _safe_body(),
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 2),
                "remote_addr": request.headers.get(
                    "X-Forwarded-For", request.remote_addr
                ),
            }
            logger.info(json.dumps(entry, ensure_ascii=False, default=str))
        except Exception:
            logger.exception("falha ao logar requisicao")
        return response
