import pytest

from modules.Telemetry import service as telemetry_service
from core.database import Database


API = "/api/v1"


def test_telemetry_creates_assessment_factors_recommendation_and_audit(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows
):
    response = client.post(
        f"{API}/telemetry",
        headers=auth_headers("operador@somple.com"),
        json=make_telemetry_payload(operation_id),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["telemetry_reading_id"] > 0
    assert 0 <= body["assessment"]["risk_score"] <= 100
    assert body["assessment"]["risk_level"] in {"low", "medium", "high", "critical"}
    assert body["assessment"]["model_version"]

    assessment = db_rows(
        "SELECT * FROM risk_assessments WHERE id = %s",
        (body["assessment"]["id"],),
    )[0]
    assert assessment["telemetry_reading_id"] == body["telemetry_reading_id"]
    assert assessment["model_version_id"] is not None
    assert assessment["explanation_summary"]
    assert assessment["input_snapshot"]
    assert assessment["output_snapshot"]

    factors = db_rows(
        "SELECT * FROM risk_factors WHERE assessment_id = %s ORDER BY rank",
        (body["assessment"]["id"],),
    )
    assert factors
    assert factors[0]["factor_label"]

    events = {
        row["event_type"]
        for row in db_rows(
            "SELECT event_type FROM audit_logs WHERE entity_id IN (%s, %s)",
            (body["telemetry_reading_id"], body["assessment"]["id"]),
        )
    }
    assert "telemetry.received" in events
    assert "risk_assessment.created" in events
    if body["alert"]["generated"]:
        assert body["alert"]["id"] is not None
        assert "alert.created" in {
            row["event_type"] for row in db_rows("SELECT event_type FROM audit_logs")
        }


def test_high_risk_branch_persists_alert_and_audit(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows, monkeypatch
):
    monkeypatch.setattr(telemetry_service, "is_high_risk", lambda _: True)

    response = client.post(
        f"{API}/telemetry",
        headers=auth_headers("admin@somple.com"),
        json=make_telemetry_payload(operation_id, scenario="critical"),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["alert"]["generated"] is True
    alert = db_rows("SELECT * FROM alerts WHERE id = %s", (body["alert"]["id"],))[0]
    assert alert["assessment_id"] == body["assessment"]["id"]
    assert alert["recommendation"]
    assert db_rows(
        "SELECT id FROM audit_logs WHERE event_type = 'alert.created' AND entity_id = %s",
        (body["alert"]["id"],),
    )


def test_audit_events_endpoint_filters_failed_login(client, auth_headers):
    client.post(
        f"{API}/auth/login",
        json={"email": "operador@somple.com", "password": "senha-invalida"},
        headers={"X-Request-ID": "audit-ui-evidence"},
    )

    response = client.get(
        f"{API}/audit/events",
        params={"event_type": "auth.login.failed"},
        headers=auth_headers("analista@somple.com"),
    )

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["event_type"] == "auth.login.failed"
    assert item["actor"] is None
    assert item["request_id"] == "audit-ui-evidence"
    assert item["metadata"] == {
        "email": "operador@somple.com",
        "reason": "invalid_credentials",
    }


def test_duplicate_telemetry_returns_conflict_without_extra_pipeline_rows(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows
):
    payload = make_telemetry_payload(operation_id)
    headers = auth_headers("operador@somple.com")
    first = client.post(f"{API}/telemetry", headers=headers, json=payload)
    duplicate = client.post(f"{API}/telemetry", headers=headers, json=payload)

    assert first.status_code == 201
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["message"] == "Telemetry event already processed"
    assert len(db_rows("SELECT id FROM telemetry_readings")) == 1
    assert len(db_rows("SELECT id FROM risk_assessments")) == 1


def test_missing_active_model_rolls_back_reading(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows
):
    with Database.transaction() as conn:
        conn.execute("UPDATE model_versions SET is_active = FALSE")

    response = client.post(
        f"{API}/telemetry",
        headers=auth_headers("operador@somple.com"),
        json=make_telemetry_payload(operation_id),
    )

    assert response.status_code == 503
    assert db_rows("SELECT id FROM telemetry_readings") == []
    assert db_rows("SELECT id FROM risk_assessments") == []


@pytest.mark.parametrize(
    ("field", "value"),
    [("source", "unknown"), ("soil_type", "unknown"), ("soil_moisture_pct", -1),
     ("soil_moisture_pct", 101), ("latitude", -91), ("longitude", 181),
     ("rainfall_mm", -1), ("speed_kmh", -1)],
)
def test_invalid_telemetry_does_not_persist(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows, field, value
):
    payload = make_telemetry_payload(operation_id)
    payload[field] = value
    response = client.post(f"{API}/telemetry", headers=auth_headers("operador@somple.com"), json=payload)
    assert response.status_code == 422
    assert db_rows("SELECT id FROM telemetry_readings") == []


def test_intermediate_failure_rolls_back_entire_pipeline(
    client, auth_headers, operation_id, make_telemetry_payload, db_rows, monkeypatch
):
    def fail_assessment(*_args, **_kwargs):
        raise RuntimeError("induced assessment failure")

    monkeypatch.setattr(telemetry_service.TelemetryRepository, "insert_assessment", fail_assessment)
    headers = auth_headers("operador@somple.com")
    with pytest.raises(RuntimeError, match="induced assessment failure"):
        client.post(
            f"{API}/telemetry",
            headers=headers,
            json=make_telemetry_payload(operation_id),
        )
    assert db_rows("SELECT id FROM telemetry_readings") == []
    assert db_rows("SELECT id FROM risk_assessments") == []
