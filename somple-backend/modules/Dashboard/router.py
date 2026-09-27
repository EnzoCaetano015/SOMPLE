from typing import Literal

from fastapi import APIRouter, Depends, Query

from core.authorization import AuthenticatedUser, require_roles
from modules.Dashboard.schemas import DashboardFilterOptions, DashboardResponse
from modules.Dashboard.service import get_dashboard, get_dashboard_filter_options

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, summary="Dashboard summary")
def dashboard(
    period: Literal["24h", "7d", "30d"] = Query(default="7d"),
    region_id: int | None = Query(default=None),
    operation_category: Literal["field", "transport", "near_water"] | None = Query(default=None),
    operation_type: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> DashboardResponse:
    return get_dashboard(
        period=period, region_id=region_id,
        operation_category=operation_category, operation_type=operation_type,
    )


@router.get(
    "/filter-options",
    response_model=DashboardFilterOptions,
    summary="Dashboard filter options",
)
def dashboard_filter_options(
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> DashboardFilterOptions:
    return get_dashboard_filter_options()
