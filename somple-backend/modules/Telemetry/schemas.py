from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CreateTelemetryRequest(BaseModel):
    operation_id: int
    recorded_at: datetime
    rainfall_mm: float = Field(ge=0)
    temperature_c: float = Field(ge=-50, le=80)
    soil_moisture_pct: float = Field(ge=0, le=100)
    soil_type: str
    slope_degrees: float = Field(ge=0, le=90)
    distance_to_water_m: float = Field(ge=0)
    speed_kmh: float = Field(ge=0)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    source: str = "simulator"


class AssessmentSummary(BaseModel):
    id: int
    risk_score: int
    risk_level: str
    confidence: float
    model_version: str


class AlertSummary(BaseModel):
    generated: bool
    id: int | None = None


class CreateTelemetryResponse(BaseModel):
    telemetry_reading_id: int
    assessment: AssessmentSummary
    alert: AlertSummary
