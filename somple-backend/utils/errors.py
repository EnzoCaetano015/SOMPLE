from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ApplicationError(Exception):
    status_code = 500
    code = "application_error"

    def __init__(self, message: str, *, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ResourceNotFoundError(ApplicationError):
    status_code = 404
    code = "resource_not_found"


class AuthenticationError(ApplicationError):
    status_code = 401
    code = "authentication_error"


class AuthorizationError(ApplicationError):
    status_code = 403
    code = "authorization_error"


class ConflictError(ApplicationError):
    status_code = 409
    code = "conflict_error"


class ValidationError(ApplicationError):
    status_code = 422
    code = "validation_error"


class ModelUnavailableError(ApplicationError):
    status_code = 503
    code = "model_unavailable"


class ApplicationFailureError(ApplicationError):
    status_code = 500
    code = "application_failure"


def _build_error_response(
    *,
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        }
    }
    if details:
        payload["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=payload)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def handle_application_error(request: Request, exc: ApplicationError) -> JSONResponse:
        return _build_error_response(
            request=request,
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        return _build_error_response(
            request=request,
            status_code=500,
            code="internal_server_error",
            message="Unexpected server error",
        )
