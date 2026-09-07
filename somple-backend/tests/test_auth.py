from core.database import Database


def _failed_login(client, email: str, password: str = "wrong-password"):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
        headers={"X-Request-ID": "pytest-login-failure"},
    )


def test_valid_login_returns_user_and_persists_success_event(client, db_rows):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@somple.com", "password": "Somple@123"},
        headers={"X-Request-ID": "pytest-login-success"},
    )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "admin"
    assert response.json()["access_token"]
    rows = db_rows("SELECT * FROM audit_logs WHERE event_type = 'auth.login'")
    assert len(rows) == 1
    assert rows[0]["actor_user_id"] is not None
    assert rows[0]["request_id"] == "pytest-login-success"
    assert rows[0]["endpoint"] == "/api/v1/auth/login"
    assert rows[0]["http_method"] == "POST"
    assert rows[0]["status_code"] == 200


def test_unknown_user_persists_generic_failure_without_secrets(client, db_rows):
    response = _failed_login(client, "naoexiste@somple.com")

    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid credentials"
    row = db_rows("SELECT * FROM audit_logs WHERE event_type = 'auth.login.failed'")[0]
    assert row["actor_user_id"] is None
    assert row["request_id"] == "pytest-login-failure"
    assert row["endpoint"] == "/api/v1/auth/login"
    assert row["http_method"] == "POST"
    assert row["status_code"] == 401
    assert row["metadata"] == {
        "email": "naoexiste@somple.com",
        "reason": "invalid_credentials",
    }
    serialized = str(row["metadata"]).lower()
    for forbidden in ("password", "senha", "hash", "token", "traceback", "stack"):
        assert forbidden not in serialized


def test_wrong_password_persists_same_generic_failure(client, db_rows):
    response = _failed_login(client, "operador@somple.com")

    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid credentials"
    row = db_rows("SELECT * FROM audit_logs WHERE event_type = 'auth.login.failed'")[0]
    assert row["actor_user_id"] is None
    assert row["metadata"]["reason"] == "invalid_credentials"


def test_inactive_user_persists_same_generic_failure(client, db_rows):
    with Database.transaction() as conn:
        conn.execute("UPDATE users SET is_active = FALSE WHERE email = 'operador@somple.com'")

    response = _failed_login(client, "operador@somple.com", "Somple@123")

    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid credentials"
    row = db_rows("SELECT * FROM audit_logs WHERE event_type = 'auth.login.failed'")[0]
    assert row["metadata"]["reason"] == "invalid_credentials"


def test_logout_requires_authentication_and_persists_event(client, auth_headers, db_rows):
    assert client.post("/api/v1/auth/logout").status_code == 401

    response = client.post(
        "/api/v1/auth/logout",
        headers=auth_headers("operador@somple.com"),
    )

    assert response.status_code == 204
    row = db_rows("SELECT * FROM audit_logs WHERE event_type = 'auth.logout'")[0]
    assert row["actor_user_id"] is not None
    assert row["status_code"] == 204
