from datetime import datetime, timedelta, timezone


API = "/api/v1"


def test_dashboard_filter_options_come_from_database(client, auth_headers):
    response = client.get(f"{API}/dashboard/filter-options", headers=auth_headers("operador@somple.com"))
    assert response.status_code == 200
    body = response.json()
    assert {item["label"] for item in body["regions"]} == {"Talhão Norte", "Talhão Leste", "Talhão Sul"}
    assert {item["value"] for item in body["operation_categories"]} == {"field", "transport", "near_water"}


def test_dashboard_applies_category_region_and_period_to_the_same_slice(
    client, auth_headers, make_telemetry_payload, db_rows
):
    operations = db_rows(
        "SELECT id, region_id, operation_category FROM operations ORDER BY id"
    )
    headers = auth_headers("operador@somple.com")
    for index, operation in enumerate(operations):
        payload = make_telemetry_payload(operation["id"], scenario="critical" if index == 0 else "normal")
        payload["recorded_at"] = (datetime.now(timezone.utc) - timedelta(minutes=index)).isoformat()
        assert client.post(f"{API}/telemetry", headers=headers, json=payload).status_code == 201

    selected = next(item for item in operations if item["operation_category"] == "transport")
    response = client.get(
        f"{API}/dashboard",
        params={"period": "24h", "region_id": selected["region_id"], "operation_category": "transport"},
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["assessment_count"] == 1
    assert body["summary"]["monitored_equipment"] == 1
    assert sum(item["count"] for item in body["risk_distribution"]) == 1
    assert sum(item["assessment_count"] for item in body["trends"]["by_operation_category"]) == 1


def test_dashboard_empty_slice_is_controlled(client, auth_headers):
    response = client.get(
        f"{API}/dashboard",
        params={"period": "24h", "region_id": 999999},
        headers=auth_headers("operador@somple.com"),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["assessment_count"] == 0
    assert body["ranking"] == []
    assert body["risk_evolution"] == []
    assert body["recent_alerts"] == []
