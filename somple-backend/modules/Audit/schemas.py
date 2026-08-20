from pydantic import BaseModel


class AuditItem(BaseModel):
    assessment_id: int
    predicted_at: str
    equipment: str
    operation: str
    score: int
    risk_level: str
    model_name: str
    model_version: str
    alert_generated: bool


class AuditResponse(BaseModel):
    items: list[AuditItem]
