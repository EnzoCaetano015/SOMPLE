"""Send simulated telemetry through the public SOMPLE API."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API_URL = "http://localhost:8000/api/v1"
DEFAULT_EMAIL = "operador@somple.com"
DEFAULT_PASSWORD = "Somple@123"

SCENARIOS: dict[str, dict[str, Any]] = {
    "normal": {
        "rainfall_mm": 1.0,
        "temperature_c": 24.0,
        "soil_moisture_pct": 38.0,
        "soil_type": "siltoso",
        "slope_degrees": 3.0,
        "distance_to_water_m": 900.0,
        "speed_kmh": 12.0,
    },
    "moderate": {
        "rainfall_mm": 25.0,
        "temperature_c": 28.0,
        "soil_moisture_pct": 68.0,
        "soil_type": "arenoso",
        "slope_degrees": 10.0,
        "distance_to_water_m": 180.0,
        "speed_kmh": 9.0,
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
}


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token: str | None = None

    def request(self, method: str, path: str, payload: dict | None = None) -> dict:
        headers = {"Accept": "application/json"}
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = Request(
            f"{self.base_url}/{path.lstrip('/')}",
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                content = response.read()
                return json.loads(content) if content else {}
        except HTTPError as exc:
            detail = _read_http_error(exc)
            raise RuntimeError(f"API returned HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Could not connect to {self.base_url}: {exc.reason}") from exc

    def login(self, email: str, password: str) -> None:
        response = self.request("POST", "/auth/login", {"email": email, "password": password})
        token = response.get("access_token")
        if not token:
            raise RuntimeError("Login response did not include an access token")
        self.token = str(token)


def _read_http_error(error: HTTPError) -> str:
    raw = error.read().decode("utf-8", errors="replace")
    if not raw:
        return error.reason
    try:
        payload = json.loads(raw)
        return str(payload.get("error", {}).get("message") or payload)
    except json.JSONDecodeError:
        return raw[:300]


def build_payload(
    scenario: str,
    operation_id: int,
    *,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    generator = rng or random.Random()
    payload = dict(SCENARIOS[scenario])
    for field, spread in {
        "rainfall_mm": 2.0,
        "temperature_c": 1.0,
        "soil_moisture_pct": 2.0,
        "slope_degrees": 1.0,
        "distance_to_water_m": 5.0,
        "speed_kmh": 1.0,
    }.items():
        payload[field] = round(max(0.0, float(payload[field]) + generator.uniform(-spread, spread)), 2)

    payload.update(
        {
            "operation_id": operation_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "latitude": -23.55052,
            "longitude": -46.633308,
            "source": "simulator",
        }
    )
    return payload


def discover_operation_ids(client: ApiClient) -> list[int]:
    equipment = client.request("GET", "/equipment").get("items", [])
    operation_ids: list[int] = []
    for item in equipment:
        code = item.get("equipment_code")
        if not code:
            continue
        detail = client.request("GET", f"/equipment/{code}")
        operation = detail.get("current_operation") or {}
        operation_id = operation.get("id")
        if operation_id is not None:
            operation_ids.append(int(operation_id))

    if not operation_ids:
        raise RuntimeError("No active operation was found. Run scripts.create_demo_data first.")
    return operation_ids


def iter_operation_ids(operation_ids: list[int]) -> Iterable[int]:
    while True:
        yield from operation_ids


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send telemetry through the SOMPLE API")
    parser.add_argument("--scenario", choices=SCENARIOS, default="normal")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--continuous", action="store_true")
    parser.add_argument("--operation-id", type=int)
    parser.add_argument("--api-url", default=os.getenv("SOMPLE_API_URL", DEFAULT_API_URL))
    parser.add_argument("--email", default=os.getenv("SOMPLE_DEMO_EMAIL", DEFAULT_EMAIL))
    parser.add_argument("--password", default=os.getenv("SOMPLE_DEMO_PASSWORD", DEFAULT_PASSWORD))
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.count < 1:
        raise ValueError("--count must be at least 1")
    if args.interval < 0:
        raise ValueError("--interval cannot be negative")
    if args.operation_id is not None and args.operation_id < 1:
        raise ValueError("--operation-id must be positive")


def run(args: argparse.Namespace, *, client: ApiClient | None = None) -> None:
    validate_args(args)
    api = client or ApiClient(args.api_url)
    api.login(args.email, args.password)
    operation_ids = [args.operation_id] if args.operation_id else discover_operation_ids(api)
    operations = iter_operation_ids(operation_ids)
    limit = None if args.continuous else args.count

    sent = 0
    while limit is None or sent < limit:
        operation_id = next(operations)
        response = api.request(
            "POST",
            "/telemetry",
            build_payload(args.scenario, operation_id),
        )
        sent += 1
        assessment = response.get("assessment", {})
        alert = response.get("alert", {})
        print(
            f"[{sent}] operation={operation_id} telemetry={response.get('telemetry_reading_id')} "
            f"score={assessment.get('risk_score')} level={assessment.get('risk_level')} "
            f"alert={alert.get('id') if alert.get('generated') else 'none'}"
        )
        if limit is None or sent < limit:
            time.sleep(args.interval)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        return 0
    except (RuntimeError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
