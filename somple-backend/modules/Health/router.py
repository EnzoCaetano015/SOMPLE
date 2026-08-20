from fastapi import APIRouter

from modules.Health.schemas import HealthReadyResponse, HealthResponse
from modules.Health.service import HealthService

router = APIRouter(prefix="/health", tags=["Healthcheck"])


@router.get("", response_model=HealthResponse, summary="Health check")
def health() -> HealthResponse:
    return HealthService.get_health()


@router.get("/ready", response_model=HealthReadyResponse, summary="Readiness check")
def ready() -> HealthReadyResponse:
    return HealthService.get_ready()
