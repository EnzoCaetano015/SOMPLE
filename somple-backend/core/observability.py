import json
import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("somple.api")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()

        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "module": _resolve_module(request.url.path),
            "status": response.status_code,
            "duration_ms": duration_ms,
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False))
        response.headers["X-Request-ID"] = request_id
        return response


def _resolve_module(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    if len(parts) >= 3 and parts[0] == "api" and parts[1] == "v1":
        return parts[2]
    return "root"


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def register_observability(app: FastAPI) -> None:
    configure_logging()
    app.add_middleware(RequestContextMiddleware)
