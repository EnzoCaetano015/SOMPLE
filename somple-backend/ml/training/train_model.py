"""
Train SOMPLE risk model from Sprint 2 dataset.
Outputs classifier + regressor bundle and metadata JSON.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "dataset_sprint2.csv"
ARTIFACTS_DIR = Path(__file__).resolve().parents[1] / "artifacts"

FEATURES = [
    "chuva_mm",
    "temperatura_c",
    "umidade_solo",
    "tipo_solo",
    "inclinacao_graus",
    "distancia_agua_m",
    "tipo_operacao",
    "peso_equipamento_t",
    "dias_desde_manutencao",
    "incidentes_previos",
]

LEVEL_MAP = {
    "baixo": "low",
    "medio": "medium",
    "alto": "high",
    "critico": "critical",
}


def build_preprocessor() -> ColumnTransformer:
    categorical = ["tipo_solo", "tipo_operacao"]
    numeric = [feature for feature in FEATURES if feature not in categorical]
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATASET_PATH)
    df["nivel_risco_en"] = df["nivel_risco"].map(LEVEL_MAP)

    X = df[FEATURES]
    y_class = df["nivel_risco_en"]
    y_score = df["score_risco"]

    preprocessor = build_preprocessor()

    classifier = Pipeline(
        steps=[
            ("preprocessador", preprocessor),
            (
                "classificador",
                RandomForestClassifier(
                    n_estimators=250,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    regressor = Pipeline(
        steps=[
            ("preprocessador", build_preprocessor()),
            ("regressor", RandomForestRegressor(n_estimators=250, random_state=42)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.25, random_state=42, stratify=y_class
    )
    _, X_score_test, _, y_score_test = train_test_split(
        X, y_score, test_size=0.25, random_state=42, stratify=y_class
    )

    classifier.fit(X_train, y_train)
    regressor.fit(X_train, y_score.loc[X_train.index])

    y_pred = classifier.predict(X_test)
    score_pred = regressor.predict(X_score_test)

    accuracy = accuracy_score(y_test, y_pred)
    reg_mae = mean_absolute_error(y_score_test, score_pred)
    reg_r2 = r2_score(y_score_test, score_pred)

    version = "1.0.0"
    model_name = "somple-risk-classifier"
    artifact_path = ARTIFACTS_DIR / f"{model_name}-v{version}.joblib"
    metadata_path = ARTIFACTS_DIR / f"{model_name}-v{version}.json"

    bundle = {
        "classifier": classifier,
        "regressor": regressor,
        "metadata": {
            "model_name": model_name,
            "version": version,
            "features": FEATURES,
            "classes": sorted(y_class.unique().tolist()),
            "metrics": {
                "accuracy": round(float(accuracy), 4),
                "regressor_mae": round(float(reg_mae), 4),
                "regressor_r2": round(float(reg_r2), 4),
            },
            "score_method": "regressor",
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "dataset_version": "sprint2-v1",
        },
    }

    joblib.dump(bundle, artifact_path)
    sha256 = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    metadata = bundle["metadata"] | {"artifact_sha256": sha256}
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"Saved: {artifact_path}")


if __name__ == "__main__":
    main()
