from typing import Any

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


class AuditEventItem(BaseModel):
    id: int
    created_at: str
    event_type: str
    actor: str | None
    entity_type: str | None
    entity_id: int | None
    request_id: str | None
    endpoint: str | None
    http_method: str | None
    status_code: int | None
    metadata: dict[str, Any]


class AuditEventsResponse(BaseModel):
    items: list[AuditEventItem]
