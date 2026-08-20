from pydantic import BaseModel


class AssessmentFactor(BaseModel):
    rank: int
    factor_code: str
    factor_label: str
    feature_name: str | None
    feature_value: object | None
    importance: float | None
    direction: str | None


class AssessmentDetailResponse(BaseModel):
    id: int
    equipment_id: str
    equipment_type: str
    operation: str
    score: int
    risk_level: str
    predicted_at: str
    model: dict
    recommendation: str | None
    factors: list[AssessmentFactor]
    inputs: dict
    alert_generated: bool
