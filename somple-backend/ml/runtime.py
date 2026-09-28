from __future__ import annotations

import json
import hashlib
from pathlib import Path

import joblib

from core.config import settings
from ml.schemas import FeatureVector, RiskPrediction
from utils.errors import ModelUnavailableError
from utils.risk import risk_level_from_score, score_from_probabilities

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

    def load(self, *, version: str | None = None, expected_sha256: str | None = None) -> None:
        if self._pipeline is not None and (version is None or self.model_version == version):
            if expected_sha256:
                self._verify_artifact_sha(self._resolve_artifact_path(version), expected_sha256)
            return

        artifact_path = self._resolve_artifact_path(version)
        metadata_path = artifact_path.with_suffix(".json")

        if not artifact_path.exists():
            raise ModelUnavailableError(f"Model artifact not found: {artifact_path.name}")

        if expected_sha256:
            self._verify_artifact_sha(artifact_path, expected_sha256)

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
            metadata_sha = self._metadata.get("artifact_sha256")
            if metadata_sha:
                self._verify_artifact_sha(artifact_path, metadata_sha)
        else:
            self.model_version = version or "1.0.0"

        if version and self.model_version != version:
            self._reset()
            raise ModelUnavailableError("Model artifact version does not match the active database version")

    def _resolve_artifact_path(self, version: str | None = None) -> Path:
        if version:
            return ARTIFACTS_DIR / f"{settings.model_name}-v{version}.joblib"
        candidates = sorted(ARTIFACTS_DIR.glob(f"{settings.model_name}-v*.joblib"))
        if candidates:
            return candidates[-1]
        legacy = ARTIFACTS_DIR / "somple-risk-classifier-v1.0.0.joblib"
        return legacy

    @staticmethod
    def _verify_artifact_sha(artifact_path: Path, expected_sha256: str) -> None:
        actual = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        if actual.lower() != expected_sha256.lower():
            raise ModelUnavailableError("Model artifact integrity check failed")

    def _reset(self) -> None:
        self._pipeline = None
        self._regressor = None
        self._metadata = None
        self.model_version = None

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

        score_method = "probability_weighted_ordinal"
        if self._regressor is not None:
            reg_score = int(round(float(self._regressor.predict(frame)[0])))
            reg_score = max(0, min(100, reg_score))
            risk_score = reg_score
            score_method = "regressor"
        else:
            risk_score, _ = score_from_probabilities(probabilities)

        risk_level = risk_level_from_score(risk_score)
        confidence = probabilities.get(risk_level, 0.0)

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
