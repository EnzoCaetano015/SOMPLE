from pydantic import BaseModel


class MonitoringSummary(BaseModel):
    total: int
    active: int
    attention: int
    critical: int


class MonitoringRow(BaseModel):
    id: str
    equipment_type: str
    operation: str
    region: str
    speed_kmh: float | None
    soil_moisture_pct: float | None
    rainfall_mm: float | None
    score: int | None
    risk_level: str | None
    last_reading_at: str | None


class MonitoringResponse(BaseModel):
    summary: MonitoringSummary
    rows: list[MonitoringRow]
