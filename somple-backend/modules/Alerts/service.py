from datetime import datetime, timezone

from fastapi import Request

from core.authorization import AuthenticatedUser
from core.database import Database
from modules.Alerts.repository import AlertsRepository
from modules.Alerts.schemas import (
    AlertItem,
    AlertsResponse,
    UpdateAlertStatusRequest,
    UpdateAlertStatusResponse,
)
from modules.Audit.service import AuditService
from utils.datetime_utils import to_iso8601
from utils.errors import ResourceNotFoundError, ValidationError


class AlertsService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = AlertsRepository()

    def list_alerts(
        self,
        *,
        status: str | None = None,
        severity: str | None = None,
        equipment_id: str | None = None,
    ) -> AlertsResponse:
        rows = self._repository.list_alerts(
            self._conn,
            {"status": status, "severity": severity, "equipment_id": equipment_id},
        )
        return AlertsResponse(
            items=[
                AlertItem(
                    id=row["id"],
                    severity=row["severity"],
                    status=row["status"],
                    title=row["title"],
                    message=row["message"],
                    recommendation=row.get("recommendation"),
                    equipment_code=row.get("equipment_code"),
                    assessment_id=row["assessment_id"],
                    created_at=to_iso8601(row["created_at"]),
                    acknowledged_at=to_iso8601(row.get("acknowledged_at")),
                    resolved_at=to_iso8601(row.get("resolved_at")),
                )
                for row in rows
            ]
        )

    def update_status(
        self,
        alert_id: int,
        payload: UpdateAlertStatusRequest,
        request: Request,
        user: AuthenticatedUser,
    ) -> UpdateAlertStatusResponse:
        alert = self._repository.get_alert(self._conn, alert_id)
        if alert is None:
            raise ResourceNotFoundError("Alert not found")

        now = datetime.now(timezone.utc)
        update_payload: dict = {"status": payload.status}
        if payload.status == "acknowledged":
            update_payload["acknowledged_by"] = user.id
            update_payload["acknowledged_at"] = now
        if payload.status == "resolved":
            update_payload["resolved_at"] = now

        row = self._repository.update_status(self._conn, alert_id, update_payload)
        event = "alert.acknowledged" if payload.status == "acknowledged" else "alert.resolved"
        if payload.status in {"acknowledged", "resolved"}:
            AuditService(self._conn).log_event(
                event_type=event,
                request=request,
                actor_user_id=user.id,
                entity_type="alert",
                entity_id=alert_id,
                status_code=200,
            )
        return UpdateAlertStatusResponse(
            id=row["id"],
            status=row["status"],
            acknowledged_at=to_iso8601(row.get("acknowledged_at")),
            resolved_at=to_iso8601(row.get("resolved_at")),
        )


def list_alerts(**filters) -> AlertsResponse:
    with Database.session() as conn:
        return AlertsService(conn).list_alerts(**filters)


def update_alert_status(
    alert_id: int,
    payload: UpdateAlertStatusRequest,
    request: Request,
    user: AuthenticatedUser,
) -> UpdateAlertStatusResponse:
    if payload.status not in {"open", "acknowledged", "resolved", "dismissed"}:
        raise ValidationError("Invalid alert status")
    with Database.transaction() as conn:
        return AlertsService(conn).update_status(alert_id, payload, request, user)
