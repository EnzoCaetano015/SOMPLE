from __future__ import annotations

import json
from pathlib import Path

import joblib

from core.config import settings
from ml.schemas import FeatureVector, RiskPrediction
from utils.errors import ModelUnavailableError
from utils.risk import score_from_probabilities

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
CLASS_LABELS = ["low", "medium", "high", "critical"]
LEVEL_MAP_PT_TO_EN = {
    "baixo": "low",
    "medio": "medium",
    "alto": "high",
    "critico": "critical",
}


class ModelRuntime:
    def __init__(self) -> None:
        self._pipeline = None
        self._regressor = None
        self._metadata: dict | None = None
        self.model_version: str | None = None
        self.model_name: str = settings.model_name

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None

    def load(self) -> None:
        if self._pipeline is not None:
            return

        artifact_path = self._resolve_artifact_path()
        metadata_path = artifact_path.with_suffix(".json")

        if not artifact_path.exists():
            raise ModelUnavailableError(f"Model artifact not found: {artifact_path.name}")

        bundle = joblib.load(artifact_path)
        if isinstance(bundle, dict):
            self._pipeline = bundle["classifier"]
            self._regressor = bundle.get("regressor")
            self._metadata = bundle.get("metadata")
        else:
            self._pipeline = bundle

        if metadata_path.exists():
            self._metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.model_version = self._metadata.get("version")
        else:
            self.model_version = "1.0.0"

    def _resolve_artifact_path(self) -> Path:
        candidates = sorted(ARTIFACTS_DIR.glob(f"{settings.model_name}-v*.joblib"))
        if candidates:
            return candidates[-1]
        legacy = ARTIFACTS_DIR / "somple-risk-classifier-v1.0.0.joblib"
        return legacy

    def predict(self, features: FeatureVector) -> RiskPrediction:
        self.load()
        assert self._pipeline is not None

        row = features.model_dump()
        frame = __import__("pandas").DataFrame([row])

        probabilities_raw = self._pipeline.predict_proba(frame)[0]
        classes = self._pipeline.classes_
        probabilities = {}
        for label, prob in zip(classes, probabilities_raw):
            normalized = LEVEL_MAP_PT_TO_EN.get(str(label), str(label))
            probabilities[normalized] = float(prob)

        for level in CLASS_LABELS:
            probabilities.setdefault(level, 0.0)

        predicted_label = self._pipeline.predict(frame)[0]
        risk_level = LEVEL_MAP_PT_TO_EN.get(str(predicted_label), str(predicted_label))
        confidence = max(probabilities.values())

        score_method = "probability_weighted_ordinal"
        if self._regressor is not None:
            reg_score = int(round(float(self._regressor.predict(frame)[0])))
            reg_score = max(0, min(100, reg_score))
            risk_score = reg_score
            score_method = "regressor"
        else:
            risk_score, derived_level = score_from_probabilities(probabilities)
            if risk_level not in probabilities or probabilities[risk_level] < 0.25:
                risk_level = derived_level

        return RiskPrediction(
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            class_probabilities=probabilities,
            model_name=self.model_name,
            model_version=self.model_version or "1.0.0",
            score_method=score_method,
        )


_runtime = ModelRuntime()


def get_model_runtime() -> ModelRuntime:
    return _runtime
