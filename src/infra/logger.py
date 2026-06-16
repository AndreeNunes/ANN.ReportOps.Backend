import os
import json
import queue
import atexit
import logging
import threading
from urllib.parse import unquote

import requests

# Mapeamento nivel do logging Python -> SeverityNumber do OpenTelemetry.
_SEVERITY = {
    logging.DEBUG: 5,
    logging.INFO: 9,
    logging.WARNING: 13,
    logging.ERROR: 17,
    logging.CRITICAL: 21,
}


class OTLPLogHandler(logging.Handler):
    """
    Handler de logging que envia os logs para um gateway OTLP/HTTP
    (ex: Grafana Cloud OTLP gateway) no formato OTLP JSON.

    O envio acontece em uma thread separada, com batching, para nao adicionar
    latencia no ciclo de request/response do Flask. Qualquer falha de rede e
    silenciada: logging nunca deve quebrar a aplicacao.
    """

    def __init__(self, endpoint, headers=None, service_name="reportops-backend",
                 env="production", batch_size=100, flush_interval=2.0, timeout=5.0):
        super().__init__()
        # OTEL_EXPORTER_OTLP_ENDPOINT e a base (.../otlp); logs vao em /v1/logs.
        self.logs_url = endpoint.rstrip("/") + "/v1/logs"
        self.service_name = service_name
        self.env = env
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.timeout = timeout

        self._queue = queue.Queue()
        self._session = requests.Session()
        self._session.headers["Content-Type"] = "application/json"
        for key, value in (headers or {}).items():
            self._session.headers[key] = value

        self._stop = threading.Event()
        self._worker = threading.Thread(
            target=self._run, name="otlp-log-worker", daemon=True
        )
        self._worker.start()
        atexit.register(self.close)

    def emit(self, record):
        try:
            ts = str(int(record.created * 1_000_000_000))  # nanossegundos
            item = (
                ts,
                record.levelname,
                _SEVERITY.get(record.levelno, 9),
                self.format(record),
            )
            self._queue.put(item)
        except Exception:
            self.handleError(record)

    def _run(self):
        while not self._stop.is_set():
            batch = self._drain(timeout=self.flush_interval)
            if batch:
                self._push(batch)
        remaining = self._drain(timeout=0)  # flush final ao encerrar
        if remaining:
            self._push(remaining)

    def _drain(self, timeout):
        batch = []
        try:
            batch.append(self._queue.get(timeout=timeout))
        except queue.Empty:
            return batch
        while len(batch) < self.batch_size:
            try:
                batch.append(self._queue.get_nowait())
            except queue.Empty:
                break
        return batch

    def _push(self, batch):
        records = [
            {
                "timeUnixNano": ts,
                "severityNumber": severity_num,
                "severityText": severity_text,
                "body": {"stringValue": line},
            }
            for ts, severity_text, severity_num, line in batch
        ]
        payload = {
            "resourceLogs": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name",
                             "value": {"stringValue": self.service_name}},
                            {"key": "deployment.environment",
                             "value": {"stringValue": self.env}},
                        ]
                    },
                    "scopeLogs": [{"scope": {}, "logRecords": records}],
                }
            ]
        }
        try:
            self._session.post(
                self.logs_url, data=json.dumps(payload), timeout=self.timeout
            )
        except Exception:
            pass  # nunca propagar erro de logging

    def close(self):
        if not self._stop.is_set():
            self._stop.set()
            self._worker.join(timeout=self.timeout + self.flush_interval)
        super().close()


def _parse_otlp_headers(raw):
    """
    Converte o valor de OTEL_EXPORTER_OTLP_HEADERS (ex:
    'Authorization=Basic%20xxx,foo=bar') em dict, fazendo o url-decode dos
    valores (o espaco vem como %20).
    """
    headers = {}
    if not raw:
        return headers
    for pair in raw.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            headers[key.strip()] = unquote(value.strip())
    return headers


def configure_logging():
    """
    Configura o logger 'reportops'. Sempre loga no console (stdout) e, se a
    variavel OTEL_EXPORTER_OTLP_ENDPOINT estiver definida, tambem envia para o
    gateway OTLP (Grafana Cloud).
    """
    logger = logging.getLogger("reportops")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter("%(message)s")

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        otlp = OTLPLogHandler(
            endpoint=endpoint,
            headers=_parse_otlp_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS")),
            service_name=os.getenv("OTEL_SERVICE_NAME", "reportops-backend"),
            env=os.getenv("APP_ENV", "production"),
        )
        otlp.setFormatter(formatter)
        logger.addHandler(otlp)
        logger.info(json.dumps({"event": "logging_started", "otlp": True}))
    else:
        logger.info(json.dumps({"event": "logging_started", "otlp": False}))

    return logger
