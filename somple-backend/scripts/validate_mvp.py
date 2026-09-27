"""Validate the running SOMPLE API through its public HTTP contract."""

from __future__ import annotations

import os
import random
import sys

from scripts.simulate_telemetry import (
    ApiClient, DEFAULT_API_URL, DEFAULT_PASSWORD,
    build_payload, discover_operation_ids,
)


def validate() -> None:
    client = ApiClient(os.getenv("SOMPLE_API_URL", DEFAULT_API_URL))
    checks: list[tuple[str, bool]] = []

    health = client.request("GET", "/health")
    checks.append(("health", health.get("status") == "ok"))
    readiness = client.request("GET", "/health/ready")
    checks.append(("readiness", readiness.get("status") == "ready"))

    client.login(
        os.getenv("SOMPLE_VALIDATION_EMAIL", "admin@somple.com"),
        os.getenv("SOMPLE_DEMO_PASSWORD", DEFAULT_PASSWORD),
    )
    operation_ids = discover_operation_ids(client)
    scenarios = ("normal", "moderate", "critical", "critical", "moderate", "critical")
    results = []
    for index, operation_id in enumerate(operation_ids):
        scenario = scenarios[index % len(scenarios)]
        payload = build_payload(scenario, operation_id, rng=random.Random(index))
        result = client.request("POST", "/telemetry", payload)
        assessment = result.get("assessment") or {}
        checks.append((f"telemetry:{scenario}", bool(assessment.get("id"))))
        results.append(result)

    dashboard = client.request("GET", "/dashboard?period=24h")
    checks.append(("dashboard", dashboard.get("summary", {}).get("assessment_count", 0) >= len(results)))
    assessment_id = results[-1]["assessment"]["id"]
    detail = client.request("GET", f"/assessments/{assessment_id}")
    checks.append(("assessment", bool(detail.get("factors")) and bool(detail.get("recommendation"))))

    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if not all(passed for _, passed in checks):
        raise RuntimeError("MVP validation failed")


def main() -> int:
    try:
        validate()
        print("SOMPLE MVP validation completed successfully.")
        return 0
    except Exception as exc:
        print(f"SOMPLE MVP validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
