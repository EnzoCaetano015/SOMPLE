from pydantic import BaseModel, Field


class FeatureVector(BaseModel):
    chuva_mm: float
    temperatura_c: float
    umidade_solo: float
    tipo_solo: str
    inclinacao_graus: float
    distancia_agua_m: float
    tipo_operacao: str
    peso_equipamento_t: float
    dias_desde_manutencao: int
    incidentes_previos: int


class RiskPrediction(BaseModel):
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    confidence: float = Field(ge=0, le=1)
    class_probabilities: dict[str, float]
    model_name: str
    model_version: str
    score_method: str
    explanation_method: str = "global_feature_importance"
