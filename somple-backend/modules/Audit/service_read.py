from datetime import datetime

from core.database import Database
from modules.Audit.repository import AuditRepository
from modules.Audit.schemas import AuditEventItem, AuditEventsResponse, AuditItem, AuditResponse
from utils.datetime_utils import to_iso8601


class AuditServiceRead:
    def __init__(self, conn):
        self._conn = conn
        self._repository = AuditRepository()

    def list_audit(
        self,
        *,
        equipment_code: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        region_id: int | None = None,
        risk_level: str | None = None,
        operation_type: str | None = None,
    ) -> AuditResponse:
        rows = self._repository.list_assessments(
            self._conn,
            {
                "equipment_code": equipment_code,
                "start_date": start_date,
                "end_date": end_date,
                "region_id": region_id,
                "risk_level": risk_level,
                "operation_type": operation_type,
            },
        )
        return AuditResponse(
            items=[
                AuditItem(
                    assessment_id=row["assessment_id"],
                    predicted_at=to_iso8601(row["predicted_at"]),
                    equipment=row["equipment"],
                    operation=row["operation"],
                    score=row["score"],
                    risk_level=row["risk_level"],
                    model_name=row["model_name"],
                    model_version=row["model_version"],
                    alert_generated=bool(row["alert_generated"]),
                )
                for row in rows
            ]
        )

    def list_events(self, *, event_type: str | None = None) -> AuditEventsResponse:
        rows = self._repository.list_events(self._conn, event_type=event_type)
        return AuditEventsResponse(
            items=[
                AuditEventItem(
                    id=row["id"],
                    created_at=to_iso8601(row["created_at"]),
                    event_type=row["event_type"],
                    actor=row["actor"],
                    entity_type=row["entity_type"],
                    entity_id=row["entity_id"],
                    request_id=row["request_id"],
                    endpoint=row["endpoint"],
                    http_method=row["http_method"],
                    status_code=row["status_code"],
                    metadata=row["metadata"] or {},
                )
                for row in rows
            ]
        )


def list_audit_history(**filters) -> AuditResponse:
    with Database.session() as conn:
        return AuditServiceRead(conn).list_audit(**filters)


def list_audit_events(*, event_type: str | None = None) -> AuditEventsResponse:
    with Database.session() as conn:
        return AuditServiceRead(conn).list_events(event_type=event_type)
