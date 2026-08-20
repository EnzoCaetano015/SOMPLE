from core.database import Database
from modules.Equipment.repository import EquipmentRepository
from modules.Equipment.schemas import EquipmentDetailResponse, EquipmentListItem, EquipmentListResponse
from utils.datetime_utils import to_iso8601
from utils.errors import ResourceNotFoundError


class EquipmentService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = EquipmentRepository()

    def list_equipment(
        self,
        *,
        search: str | None = None,
        region_id: int | None = None,
        risk_level: str | None = None,
    ) -> EquipmentListResponse:
        rows = self._repository.list_equipment(
            self._conn,
            {"search": search, "region_id": region_id, "risk_level": risk_level},
        )
        items = [
            EquipmentListItem(
                equipment_code=row["equipment_code"],
                equipment_type=row["equipment_type"],
                region_name=row.get("region_name"),
                equipment_status=row["equipment_status"],
                risk_score=row.get("risk_score"),
                risk_level=row.get("risk_level"),
                last_reading_at=to_iso8601(row.get("recorded_at")),
            )
            for row in rows
        ]
        return EquipmentListResponse(items=items, total=len(items))

    def get_detail(self, equipment_code: str) -> EquipmentDetailResponse:
        row = self._repository.get_by_code(self._conn, equipment_code)
        if row is None:
            raise ResourceNotFoundError("Equipment not found")

        return EquipmentDetailResponse(
            equipment={
                "code": row["equipment_code"],
                "type": row["equipment_type"],
                "status": row["equipment_status"],
            },
            current_operation={
                "id": row.get("operation_id"),
                "type": row.get("operation_type"),
                "category": row.get("operation_category"),
                "status": row.get("operation_status"),
            }
            if row.get("operation_id")
            else None,
            region={"id": row.get("region_id"), "name": row.get("region_name")}
            if row.get("region_id")
            else None,
            latest_telemetry={
                "speed_kmh": row.get("speed_kmh"),
                "soil_moisture_pct": row.get("soil_moisture_pct"),
                "rainfall_mm": row.get("rainfall_mm"),
                "recorded_at": to_iso8601(row.get("recorded_at")),
            }
            if row.get("telemetry_reading_id")
            else None,
            latest_assessment={
                "id": row.get("assessment_id"),
                "risk_score": row.get("risk_score"),
                "risk_level": row.get("risk_level"),
                "confidence": float(row["confidence"]) if row.get("confidence") is not None else None,
                "predicted_at": to_iso8601(row.get("predicted_at")),
                "model_version": row.get("model_version"),
            }
            if row.get("assessment_id")
            else None,
        )


def list_equipment(**filters) -> EquipmentListResponse:
    with Database.session() as conn:
        return EquipmentService(conn).list_equipment(**filters)


def get_equipment_detail(equipment_code: str) -> EquipmentDetailResponse:
    with Database.session() as conn:
        return EquipmentService(conn).get_detail(equipment_code)
