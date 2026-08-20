from core.database import Database
from modules.Monitoring.repository import MonitoringRepository
from modules.Monitoring.schemas import MonitoringResponse, MonitoringRow, MonitoringSummary
from utils.datetime_utils import to_iso8601


class MonitoringService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = MonitoringRepository()

    def list_monitoring(
        self,
        *,
        region_id: int | None = None,
        risk_level: str | None = None,
    ) -> MonitoringResponse:
        rows = self._repository.fetch_rows(
            self._conn, {"region_id": region_id, "risk_level": risk_level}
        )
        return MonitoringResponse(
            summary=MonitoringSummary(
                total=len(rows),
                active=len([r for r in rows if r.get("equipment_status") == "active"]),
                attention=len([r for r in rows if r.get("risk_level") in ("medium", "high")]),
                critical=len([r for r in rows if r.get("risk_level") == "critical"]),
            ),
            rows=[
                MonitoringRow(
                    id=row["equipment_code"],
                    equipment_type=row["equipment_type"],
                    operation=row.get("operation_type") or "",
                    region=row.get("region_name") or "",
                    speed_kmh=float(row["speed_kmh"]) if row.get("speed_kmh") is not None else None,
                    soil_moisture_pct=float(row["soil_moisture_pct"])
                    if row.get("soil_moisture_pct") is not None
                    else None,
                    rainfall_mm=float(row["rainfall_mm"]) if row.get("rainfall_mm") is not None else None,
                    score=row.get("risk_score"),
                    risk_level=row.get("risk_level"),
                    last_reading_at=to_iso8601(row.get("recorded_at")),
                )
                for row in rows
            ],
        )


def list_monitoring(**filters) -> MonitoringResponse:
    with Database.session() as conn:
        return MonitoringService(conn).list_monitoring(**filters)
