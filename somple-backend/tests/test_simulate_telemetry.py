from __future__ import annotations

import argparse
import ast
import io
import json
import random
from pathlib import Path

import pytest

from scripts import simulate_telemetry as simulator


class FakeClient:
    def __init__(self):
        self.login_args = None
        self.calls = []

    def login(self, email, password):
        self.login_args = (email, password)

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if path == "/equipment":
            return {"items": [{"equipment_code": "EQ-001"}]}
        if path == "/equipment/EQ-001":
            return {"current_operation": {"id": 7}}
        return {
            "telemetry_reading_id": 1,
            "assessment": {"risk_score": 42, "risk_level": "medium"},
            "alert": {"generated": False, "id": None},
        }


@pytest.mark.parametrize("scenario", ["normal", "moderate", "critical"])
def test_payloads_are_valid_and_identify_scenario(scenario):
    payload = simulator.build_payload(scenario, 9, rng=random.Random(1))

    assert payload["operation_id"] == 9
    assert payload["source"] == "simulator"
    assert payload["recorded_at"].endswith("+00:00")
    assert 0 <= payload["soil_moisture_pct"] <= 100
    assert -90 <= payload["latitude"] <= 90
    assert -180 <= payload["longitude"] <= 180


def test_run_authenticates_discovers_operations_and_posts_only_to_telemetry(monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(simulator.time, "sleep", lambda _: None)
    args = argparse.Namespace(
        scenario="normal",
        count=2,
        interval=0,
        continuous=False,
        operation_id=None,
        api_url="http://example.test/api/v1",
        email="operador@somple.com",
        password="secret",
    )

    simulator.run(args, client=client)

    assert client.login_args == ("operador@somple.com", "secret")
    assert [(method, path) for method, path, _ in client.calls] == [
        ("GET", "/equipment"),
        ("GET", "/equipment/EQ-001"),
        ("POST", "/telemetry"),
        ("POST", "/telemetry"),
    ]


def test_explicit_operation_skips_discovery():
    client = FakeClient()
    args = argparse.Namespace(
        scenario="critical",
        count=1,
        interval=0,
        continuous=False,
        operation_id=23,
        api_url="http://example.test/api/v1",
        email="admin@somple.com",
        password="secret",
    )

    simulator.run(args, client=client)

    assert [(method, path) for method, path, _ in client.calls] == [("POST", "/telemetry")]
    assert client.calls[0][2]["operation_id"] == 23


@pytest.mark.parametrize(
    ("count", "interval", "operation_id", "message"),
    [(0, 1, None, "--count"), (1, -1, None, "--interval"), (1, 1, 0, "--operation-id")],
)
def test_invalid_arguments_are_rejected(count, interval, operation_id, message):
    args = argparse.Namespace(count=count, interval=interval, operation_id=operation_id)
    with pytest.raises(ValueError, match=message):
        simulator.validate_args(args)


def test_api_client_sends_json_and_bearer_token(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def read(self):
            return json.dumps({"ok": True}).encode()

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(simulator, "urlopen", fake_urlopen)
    client = simulator.ApiClient("http://example.test/api/v1", timeout=4)
    client.token = "jwt-token"

    assert client.request("POST", "/telemetry", {"operation_id": 1}) == {"ok": True}
    request = captured["request"]
    assert request.full_url == "http://example.test/api/v1/telemetry"
    assert request.method == "POST"
    assert request.headers["Authorization"] == "Bearer jwt-token"
    assert json.loads(request.data) == {"operation_id": 1}
    assert captured["timeout"] == 4


def test_login_requires_access_token(monkeypatch):
    client = simulator.ApiClient("http://example.test")
    monkeypatch.setattr(client, "request", lambda *_args, **_kwargs: {})
    with pytest.raises(RuntimeError, match="access token"):
        client.login("operador@somple.com", "secret")


def test_simulator_has_no_database_or_repository_imports():
    source_path = Path(simulator.__file__)
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name.lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append((node.module or "").lower())

    assert not any("database" in name or "repository" in name for name in imported)
    source = source_path.read_text(encoding="utf-8").lower()
    assert "psycopg" not in source
