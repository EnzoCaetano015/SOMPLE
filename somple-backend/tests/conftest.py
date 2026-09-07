from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg.rows import dict_row


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://somple_test:somple_test@localhost:5433/somple_test",
)


def _assert_test_database(url: str) -> None:
    database_name = urlparse(url).path.lstrip("/").lower()
    if not database_name or "test" not in database_name:
        raise RuntimeError(
            "Refusing to run destructive tests: TEST_DATABASE_URL must target a database whose name contains 'test'."
        )


_assert_test_database(TEST_DATABASE_URL)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5433")
os.environ.setdefault("DB_NAME", "somple_test")
os.environ.setdefault("DB_USER", "somple_test")
os.environ.setdefault("DB_PASSWORD", "somple_test")
os.environ.setdefault("JWT_SECRET_KEY", "somple-test-secret-key-at-least-32-bytes")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXP_HOURS", "1")
os.environ.setdefault("MODEL_NAME", "somple-risk-classifier")

from core.database import Database, close_database_pool  # noqa: E402
from main import app  # noqa: E402
from scripts.create_demo_data import DEMO_PASSWORD, upsert_demo_data  # noqa: E402


MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "somple-infra" / "database" / "migrations"
TABLES = (
    "audit_logs",
    "alerts",
    "risk_factors",
    "risk_assessments",
    "telemetry_readings",
    "maintenance_records",
    "operations",
    "equipment",
    "model_versions",
    "users",
    "regions",
    "customers",
)


def _apply_migrations_if_needed() -> None:
    with psycopg.connect(TEST_DATABASE_URL, autocommit=True) as conn:
        exists = conn.execute("SELECT to_regclass('public.users')").fetchone()[0]
        if exists:
            return
        for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
            conn.execute(migration.read_text(encoding="utf-8"))


@pytest.fixture(scope="session", autouse=True)
def prepared_database():
    _apply_migrations_if_needed()
    yield
    close_database_pool()


@pytest.fixture(autouse=True)
def reset_database(prepared_database):
    with Database.transaction() as conn:
        conn.execute(f"TRUNCATE TABLE {', '.join(TABLES)} RESTART IDENTITY CASCADE")
    upsert_demo_data()


@pytest.fixture
def client(reset_database):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def login(client):
    def _login(email: str, password: str = DEMO_PASSWORD) -> dict:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, response.text
        return response.json()

    return _login


@pytest.fixture
def auth_headers(login):
    def _headers(email: str) -> dict[str, str]:
        token = login(email)["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
def operation_id() -> int:
    with Database.session() as conn:
        return conn.execute("SELECT id FROM operations ORDER BY id LIMIT 1").fetchone()["id"]


def telemetry_payload(operation_id: int, *, scenario: str = "normal") -> dict:
    values = {
        "normal": {
            "rainfall_mm": 1.0,
            "temperature_c": 24.0,
            "soil_moisture_pct": 38.0,
            "soil_type": "siltoso",
            "slope_degrees": 3.0,
            "distance_to_water_m": 900.0,
            "speed_kmh": 12.0,
        },
        "critical": {
            "rainfall_mm": 60.0,
            "temperature_c": 31.0,
            "soil_moisture_pct": 96.0,
            "soil_type": "argiloso",
            "slope_degrees": 24.0,
            "distance_to_water_m": 15.0,
            "speed_kmh": 7.0,
        },
    }[scenario]
    return {
        "operation_id": operation_id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        **values,
        "latitude": -23.55052,
        "longitude": -46.633308,
        "source": "simulator",
    }


@pytest.fixture
def make_telemetry_payload():
    return telemetry_payload


@pytest.fixture
def db_rows():
    def _rows(query: str, params: tuple = ()) -> list[dict]:
        with psycopg.connect(TEST_DATABASE_URL, row_factory=dict_row) as conn:
            return conn.execute(query, params).fetchall()

    return _rows
