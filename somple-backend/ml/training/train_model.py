"""Reproducible training pipeline for the SOMPLE risk model."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_fscore_support,
    r2_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "dataset_sprint2.csv"
ARTIFACTS_DIR = Path(__file__).resolve().parents[1] / "artifacts"
REPORTS_DIR = BASE_DIR / "reports"
MODEL_NAME = "somple-risk-classifier"
MODEL_VERSION = "1.1.0"
DATASET_VERSION = "dataset-v1-reviewed"

FEATURES = [
    "chuva_mm", "temperatura_c", "umidade_solo", "tipo_solo",
    "inclinacao_graus", "distancia_agua_m", "tipo_operacao",
    "peso_equipamento_t", "dias_desde_manutencao", "incidentes_previos",
]
TARGETS = ["score_risco", "nivel_risco"]
EXPECTED_COLUMNS = set(FEATURES + TARGETS)
CATEGORICAL_VALUES = {
    "tipo_solo": {"arenoso", "argiloso", "misto", "siltoso"},
    "tipo_operacao": {"colheita", "plantio", "pulverizacao", "transporte"},
    "nivel_risco": {"baixo", "medio", "alto", "critico"},
}
PHYSICAL_RANGES = {
    "chuva_mm": (0, None), "temperatura_c": (-50, 80), "umidade_solo": (0, 100),
    "inclinacao_graus": (0, 90), "distancia_agua_m": (0, None),
    "peso_equipamento_t": (0, None), "dias_desde_manutencao": (0, None),
    "incidentes_previos": (0, None), "score_risco": (0, 100),
}
LEVEL_MAP = {"baixo": "low", "medio": "medium", "alto": "high", "critico": "critical"}
CLASS_ORDER = ["low", "medium", "high", "critical"]


def load_dataset(path: Path = DATASET_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def validate_dataset(df: pd.DataFrame) -> dict[str, Any]:
    missing_columns = sorted(EXPECTED_COLUMNS - set(df.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing_columns)}")
    if df.empty:
        raise ValueError("Dataset is empty")
    null_counts = df[list(EXPECTED_COLUMNS)].isna().sum()
    invalid_nulls = {key: int(value) for key, value in null_counts.items() if value}
    if invalid_nulls:
        raise ValueError(f"Dataset contains null values: {invalid_nulls}")
    duplicates = int(df.duplicated().sum())
    if duplicates:
        raise ValueError(f"Dataset contains {duplicates} duplicate rows")

    for column, allowed in CATEGORICAL_VALUES.items():
        unknown = sorted(set(df[column].astype(str)) - allowed)
        if unknown:
            raise ValueError(f"Dataset contains invalid {column} categories: {unknown}")
    for column, (minimum, maximum) in PHYSICAL_RANGES.items():
        values = pd.to_numeric(df[column], errors="coerce")
        if values.isna().any():
            raise ValueError(f"Dataset column {column} must be numeric")
        if minimum is not None and (values < minimum).any():
            raise ValueError(f"Dataset column {column} contains values below {minimum}")
        if maximum is not None and (values > maximum).any():
            raise ValueError(f"Dataset column {column} contains values above {maximum}")

    distribution = df["nivel_risco"].value_counts().sort_index().to_dict()
    if min(distribution.values()) < 2:
        raise ValueError("Each risk class needs at least two rows for stratified evaluation")
    return {
        "rows": int(len(df)), "columns": int(len(df.columns)), "null_values": 0,
        "duplicate_rows": 0,
        "class_distribution": {str(key): int(value) for key, value in distribution.items()},
        "categorical_values": {
            column: sorted(df[column].astype(str).unique().tolist())
            for column in CATEGORICAL_VALUES
        },
    }


def prepare_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    prepared = df.copy()
    prepared["nivel_risco_en"] = prepared["nivel_risco"].map(LEVEL_MAP)
    return prepared[FEATURES], prepared["nivel_risco_en"], prepared["score_risco"]


def build_preprocessor() -> ColumnTransformer:
    categorical = ["tipo_solo", "tipo_operacao"]
    numeric = [feature for feature in FEATURES if feature not in categorical]
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric),
    ])


def build_models() -> tuple[Pipeline, Pipeline]:
    classifier = Pipeline([
        ("preprocessador", build_preprocessor()),
        ("classificador", RandomForestClassifier(
            n_estimators=250, random_state=42, class_weight="balanced"
        )),
    ])
    regressor = Pipeline([
        ("preprocessador", build_preprocessor()),
        ("regressor", RandomForestRegressor(n_estimators=250, random_state=42)),
    ])
    return classifier, regressor


def evaluate_models(
    classifier: Pipeline, regressor: Pipeline, X: pd.DataFrame,
    y_class: pd.Series, y_score: pd.Series,
) -> dict[str, Any]:
    splitter = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    class_predictions = np.empty(len(X), dtype=object)
    score_predictions = np.empty(len(X), dtype=float)
    fold_sizes: list[dict[str, int]] = []
    for train_index, test_index in splitter.split(X, y_class):
        fold_classifier, fold_regressor = clone(classifier), clone(regressor)
        fold_classifier.fit(X.iloc[train_index], y_class.iloc[train_index])
        fold_regressor.fit(X.iloc[train_index], y_score.iloc[train_index])
        class_predictions[test_index] = fold_classifier.predict(X.iloc[test_index])
        score_predictions[test_index] = fold_regressor.predict(X.iloc[test_index])
        fold_sizes.append({"train": int(len(train_index)), "test": int(len(test_index))})

    precision, recall, f1, support = precision_recall_fscore_support(
        y_class, class_predictions, labels=CLASS_ORDER, zero_division=0
    )
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        y_class, class_predictions, average="macro", zero_division=0
    )
    matrix = confusion_matrix(y_class, class_predictions, labels=CLASS_ORDER)
    return {
        "classifier": {
            "accuracy": round(float(accuracy_score(y_class, class_predictions)), 4),
            "precision_macro": round(float(macro_precision), 4),
            "recall_macro": round(float(macro_recall), 4),
            "f1_macro": round(float(macro_f1), 4),
            "per_class": {
                label: {"precision": round(float(precision[index]), 4),
                        "recall": round(float(recall[index]), 4),
                        "f1": round(float(f1[index]), 4), "support": int(support[index])}
                for index, label in enumerate(CLASS_ORDER)
            },
            "confusion_matrix": matrix.tolist(), "confusion_matrix_labels": CLASS_ORDER,
        },
        "regressor": {
            "mae": round(float(mean_absolute_error(y_score, score_predictions)), 4),
            "rmse": round(float(mean_squared_error(y_score, score_predictions) ** 0.5), 4),
            "r2": round(float(r2_score(y_score, score_predictions)), 4),
        },
        "evaluation": {"method": "2-fold stratified out-of-fold evaluation",
                       "fold_sizes": fold_sizes, "final_fit_size": int(len(X)), "random_state": 42},
    }


def train_models(
    classifier: Pipeline, regressor: Pipeline, X: pd.DataFrame,
    y_class: pd.Series, y_score: pd.Series,
) -> tuple[Pipeline, Pipeline]:
    classifier.fit(X, y_class)
    regressor.fit(X, y_score)
    return classifier, regressor


def save_reports(metadata: dict[str, Any], quality: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {"dataset_quality": quality, **metadata}
    (REPORTS_DIR / f"model-v{MODEL_VERSION}-evaluation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    classifier_metrics = metadata["metrics"]["classifier"]
    labels = classifier_metrics["confusion_matrix_labels"]
    rows = "\n".join(
        f"| {label} | " + " | ".join(str(value) for value in row) + " |"
        for label, row in zip(labels, classifier_metrics["confusion_matrix"])
    )
    markdown = f"""# SOMPLE model v{MODEL_VERSION} evaluation

Metrics use 2-fold stratified out-of-fold predictions because the smallest class has only two examples. The final artifact is fitted with all {quality['rows']} rows.

## Metrics

```json
{json.dumps(metadata['metrics'], indent=2, ensure_ascii=False)}
```

## Confusion matrix

| actual \\ predicted | {' | '.join(labels)} |
| --- | {' | '.join('---' for _ in labels)} |
{rows}

The simulated academic dataset is small; these metrics do not represent production performance.
"""
    (REPORTS_DIR / f"model-v{MODEL_VERSION}-evaluation.md").write_text(markdown, encoding="utf-8")


def save_artifacts(
    classifier: Pipeline, regressor: Pipeline, metrics: dict[str, Any], quality: dict[str, Any]
) -> dict[str, Any]:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACTS_DIR / f"{MODEL_NAME}-v{MODEL_VERSION}.joblib"
    metadata_path = artifact_path.with_suffix(".json")
    metadata = {
        "model_name": MODEL_NAME, "version": MODEL_VERSION, "features": FEATURES,
        "classes": CLASS_ORDER, "metrics": metrics,
        "score_method": "regressor_with_threshold_policy",
        "risk_policy_version": "score-thresholds-v1",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "dataset_version": DATASET_VERSION, "dataset_quality": quality,
    }
    joblib.dump({"classifier": classifier, "regressor": regressor, "metadata": metadata}, artifact_path)
    metadata["artifact_sha256"] = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    save_reports(metadata, quality)
    return metadata


def main() -> None:
    df = load_dataset()
    quality = validate_dataset(df)
    X, y_class, y_score = prepare_dataset(df)
    classifier, regressor = build_models()
    metrics = evaluate_models(classifier, regressor, X, y_class, y_score)
    classifier, regressor = train_models(classifier, regressor, X, y_class, y_score)
    print(json.dumps(save_artifacts(classifier, regressor, metrics, quality), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
