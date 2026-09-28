import pytest


API = "/api/v1"


@pytest.mark.parametrize(
    "path",
    ["/dashboard", "/dashboard/filter-options", "/equipment", "/operations", "/monitoring", "/alerts", "/audit", "/audit/events"],
)
def test_protected_reads_require_authentication(client, path):
    assert client.get(f"{API}{path}").status_code == 401
    assert client.get(f"{API}{path}", headers={"Authorization": "Bearer invalid"}).status_code == 401


def test_health_and_login_are_public(client):
    assert client.get(f"{API}/health").status_code == 200
    assert client.post(
        f"{API}/auth/login",
        json={"email": "operador@somple.com", "password": "Somple@123"},
    ).status_code == 200


@pytest.mark.parametrize("email", ["admin@somple.com", "analista@somple.com", "operador@somple.com"])
@pytest.mark.parametrize("path", ["/dashboard", "/equipment", "/operations", "/monitoring", "/alerts"])
def test_all_roles_can_read_operational_routes(client, auth_headers, email, path):
    assert client.get(f"{API}{path}", headers=auth_headers(email)).status_code == 200


def test_operator_is_forbidden_from_analytical_routes(client, auth_headers, operation_id, make_telemetry_payload):
    headers = auth_headers("operador@somple.com")
    telemetry = client.post(
        f"{API}/telemetry",
        headers=headers,
        json=make_telemetry_payload(operation_id),
    )
    assert telemetry.status_code == 201
    assessment_id = telemetry.json()["assessment"]["id"]

    assert client.get(f"{API}/audit", headers=headers).status_code == 403
    assert client.get(f"{API}/audit/events", headers=headers).status_code == 403
    assert client.get(f"{API}/assessments/{assessment_id}", headers=headers).status_code == 403


@pytest.mark.parametrize("email", ["admin@somple.com", "analista@somple.com"])
def test_admin_and_analyst_can_read_analytical_routes(
    client, auth_headers, email, operation_id, make_telemetry_payload
):
    operator_headers = auth_headers("operador@somple.com")
    created = client.post(
        f"{API}/telemetry",
        headers=operator_headers,
        json=make_telemetry_payload(operation_id),
    ).json()
    headers = auth_headers(email)

    assert client.get(f"{API}/audit", headers=headers).status_code == 200
    assert client.get(f"{API}/audit/events", headers=headers).status_code == 200
    assert client.get(f"{API}/assessments/{created['assessment']['id']}", headers=headers).status_code == 200


def test_analyst_cannot_send_telemetry(client, auth_headers, operation_id, make_telemetry_payload):
    response = client.post(
        f"{API}/telemetry",
        headers=auth_headers("analista@somple.com"),
        json=make_telemetry_payload(operation_id),
    )
    assert response.status_code == 403


@pytest.mark.parametrize("email", ["admin@somple.com", "operador@somple.com"])
def test_admin_and_operator_can_send_telemetry(
    client, auth_headers, email, operation_id, make_telemetry_payload
):
    response = client.post(
        f"{API}/telemetry",
        headers=auth_headers(email),
        json=make_telemetry_payload(operation_id),
    )
    assert response.status_code == 201


def test_alert_status_matrix(client, auth_headers, operation_id, make_telemetry_payload, db_rows):
    created = client.post(
        f"{API}/telemetry",
        headers=auth_headers("operador@somple.com"),
        json=make_telemetry_payload(operation_id, scenario="critical"),
    ).json()
    alert_id = created["alert"]["id"]
    if alert_id is None:
        alert_id = db_rows(
            """
            INSERT INTO alerts (assessment_id, severity, title, message, status)
            VALUES (%s, 'critical', 'Teste RBAC', 'Teste RBAC', 'open')
            RETURNING id
            """,
            (created["assessment"]["id"],),
        )[0]["id"]

    operator = client.patch(
        f"{API}/alerts/{alert_id}/status",
        headers=auth_headers("operador@somple.com"),
        json={"status": "acknowledged"},
    )
    analyst = client.patch(
        f"{API}/alerts/{alert_id}/status",
        headers=auth_headers("analista@somple.com"),
        json={"status": "acknowledged"},
    )
    admin = client.patch(
        f"{API}/alerts/{alert_id}/status",
        headers=auth_headers("admin@somple.com"),
        json={"status": "resolved"},
    )

    assert operator.status_code == 403
    assert analyst.status_code == 200
    assert admin.status_code == 200
