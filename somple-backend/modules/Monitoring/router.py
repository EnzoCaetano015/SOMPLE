from fastapi import APIRouter, Depends, Query

from core.authorization import AuthenticatedUser, require_roles
from modules.Monitoring.schemas import MonitoringResponse
from modules.Monitoring.service import list_monitoring

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.get("", response_model=MonitoringResponse, summary="Monitoring table")
def monitoring(
    region_id: int | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> MonitoringResponse:
    return list_monitoring(region_id=region_id, risk_level=risk_level)
