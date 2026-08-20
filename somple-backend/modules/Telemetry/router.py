from fastapi import APIRouter, Depends, Request, status

from core.authorization import AuthenticatedUser, require_authenticated_user
from modules.Telemetry.schemas import CreateTelemetryRequest, CreateTelemetryResponse
from modules.Telemetry.service import create_telemetry

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post(
    "",
    response_model=CreateTelemetryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest telemetry and run risk pipeline",
)
def post_telemetry(
    payload: CreateTelemetryRequest,
    request: Request,
    user: AuthenticatedUser = Depends(require_authenticated_user),
) -> CreateTelemetryResponse:
    return create_telemetry(payload, request, user)
