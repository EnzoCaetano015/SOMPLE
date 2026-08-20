from pydantic import BaseModel


class OperationItem(BaseModel):
    key: str
    name: str
    region_id: int
    region_name: str
    equipment_count: int
    average_risk_score: int
    risk_level: str
    status: str


class OperationsResponse(BaseModel):
    items: list[OperationItem]
