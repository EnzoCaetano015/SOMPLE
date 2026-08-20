from datetime import datetime

from core.database import Database
from modules.Audit.repository import AuditRepository
from modules.Audit.schemas import AuditItem, AuditResponse
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


def list_audit_history(**filters) -> AuditResponse:
    with Database.session() as conn:
        return AuditServiceRead(conn).list_audit(**filters)
