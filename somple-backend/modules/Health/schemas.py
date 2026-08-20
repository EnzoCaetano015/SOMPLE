from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class HealthReadyResponse(BaseModel):
    status: str
    database: str
    model: str
    model_version: str | None = None
