from pydantic import BaseModel


class EquipmentListItem(BaseModel):
    equipment_code: str
    equipment_type: str
    region_name: str | None
    equipment_status: str
    risk_score: int | None
    risk_level: str | None
    last_reading_at: str | None


class EquipmentListResponse(BaseModel):
    items: list[EquipmentListItem]
    total: int


class EquipmentDetailResponse(BaseModel):
    equipment: dict
    current_operation: dict | None
    region: dict | None
    latest_telemetry: dict | None
    latest_assessment: dict | None
