from fastapi import APIRouter, Depends, Query, Request

from core.authorization import AuthenticatedUser, require_roles
from modules.Alerts.schemas import AlertsResponse, UpdateAlertStatusRequest, UpdateAlertStatusResponse
from modules.Alerts.service import list_alerts, update_alert_status

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=AlertsResponse, summary="List alerts")
def alerts(
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    equipment_id: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> AlertsResponse:
    return list_alerts(status=status, severity=severity, equipment_id=equipment_id)


@router.patch("/{alert_id}/status", response_model=UpdateAlertStatusResponse, summary="Update alert status")
def patch_alert_status(
    alert_id: int,
    payload: UpdateAlertStatusRequest,
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin", "analyst")),
) -> UpdateAlertStatusResponse:
    return update_alert_status(alert_id, payload, request, user)
