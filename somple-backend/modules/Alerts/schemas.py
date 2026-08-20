from pydantic import BaseModel, Field


class AlertItem(BaseModel):
    id: int
    severity: str
    status: str
    title: str
    message: str
    recommendation: str | None
    equipment_code: str | None
    assessment_id: int
    created_at: str
    acknowledged_at: str | None = None
    resolved_at: str | None = None


class AlertsResponse(BaseModel):
    items: list[AlertItem]


class UpdateAlertStatusRequest(BaseModel):
    status: str = Field(pattern="^(acknowledged|resolved|dismissed|open)$")


class UpdateAlertStatusResponse(BaseModel):
    id: int
    status: str
    acknowledged_at: str | None = None
    resolved_at: str | None = None
