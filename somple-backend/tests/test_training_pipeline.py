import pytest
import json
from pathlib import Path

from ml.training.train_model import load_dataset, prepare_dataset, validate_dataset
from ml.runtime import ModelRuntime


def test_dataset_schema_and_quality_are_valid():
    quality = validate_dataset(load_dataset())
    assert quality["rows"] == 180
    assert quality["null_values"] == 0
    assert quality["duplicate_rows"] == 0


def test_dataset_missing_column_is_rejected():
    frame = load_dataset().drop(columns=["tipo_solo"])
    with pytest.raises(ValueError, match="missing required columns"):
        validate_dataset(frame)


def test_dataset_unknown_category_is_rejected():
    frame = load_dataset()
    frame.loc[0, "tipo_solo"] = "desconhecido"
    with pytest.raises(ValueError, match="invalid tipo_solo categories"):
        validate_dataset(frame)


def test_prepared_dataset_contains_all_features():
    X, y_class, y_score = prepare_dataset(load_dataset())
    assert len(X) == len(y_class) == len(y_score) == 180
    assert set(y_class.unique()) == {"low", "medium", "high", "critical"}


def test_final_artifact_integrity_and_runtime_loading():
    metadata_path = Path(__file__).resolve().parents[1] / "ml" / "artifacts" / "somple-risk-classifier-v1.1.0.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    runtime = ModelRuntime()
    runtime.load(version="1.1.0", expected_sha256=metadata["artifact_sha256"])
    assert runtime.is_loaded
    assert runtime.model_version == "1.1.0"
