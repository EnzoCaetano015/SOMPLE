from fastapi import APIRouter, Depends, Query

from core.authorization import AuthenticatedUser, require_roles
from modules.Dashboard.schemas import DashboardResponse
from modules.Dashboard.service import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, summary="Dashboard summary")
def dashboard(
    period: str | None = Query(default=None),
    region_id: int | None = Query(default=None),
    operation_type: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> DashboardResponse:
    return get_dashboard(period=period, region_id=region_id, operation_type=operation_type)
