"""
Populate local development database with demo users, equipment and operations.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.config import settings
from core.database import Database, init_database_pool, close_database_pool
from core.security import hash_password

ARTIFACTS_DIR = Path(__file__).resolve().parents[1] / "ml" / "artifacts"
DEMO_PASSWORD = "Somple@123"


def upsert_demo_data() -> None:
    password_hash = hash_password(DEMO_PASSWORD)
    now = datetime.now(timezone.utc)

    with Database.transaction() as conn:
        conn.execute(
            """
            INSERT INTO customers (external_code, name)
            VALUES ('DEMO-001', 'Fazenda Demonstração SOMPLE')
            ON CONFLICT (external_code) DO NOTHING
            """
        )
        customer = conn.execute(
            "SELECT id FROM customers WHERE external_code = 'DEMO-001'"
        ).fetchone()

        for region_name in ("Talhão Norte", "Talhão Leste", "Talhão Sul"):
            conn.execute(
                """
                INSERT INTO regions (customer_id, name, state_code)
                VALUES (%s, %s, 'SP')
                ON CONFLICT (customer_id, name) DO NOTHING
                """,
                (customer["id"], region_name),
            )

        users = [
            ("Administrador SOMPLE", "admin@somple.com", "admin"),
            ("Analista SOMPLE", "analista@somple.com", "analyst"),
            ("Operador SOMPLE", "operador@somple.com", "operator"),
        ]
        for name, email, role in users:
            conn.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE
                SET password_hash = EXCLUDED.password_hash, role = EXCLUDED.role, name = EXCLUDED.name
                """,
                (name, email, password_hash, role),
            )

        equipment_specs = [
            ("EQ-001", "colheitadeira", 11.2, "Talhão Norte"),
            ("EQ-002", "pulverizador", 8.5, "Talhão Leste"),
            ("EQ-003", "trator", 9.8, "Talhão Sul"),
            ("EQ-004", "colheitadeira", 12.4, "Talhão Norte"),
            ("EQ-005", "plantadeira", 7.6, "Talhão Leste"),
            ("EQ-006", "trator", 10.1, "Talhão Sul"),
        ]

        for code, eq_type, weight, region_name in equipment_specs:
            region = conn.execute(
                "SELECT id FROM regions WHERE customer_id = %s AND name = %s",
                (customer["id"], region_name),
            ).fetchone()
            conn.execute(
                """
                INSERT INTO equipment (
                    customer_id, current_region_id, external_code,
                    equipment_type, weight_tons, status
                )
                VALUES (%s, %s, %s, %s, %s, 'active')
                ON CONFLICT (customer_id, external_code) DO UPDATE
                SET equipment_type = EXCLUDED.equipment_type, weight_tons = EXCLUDED.weight_tons
                """,
                (customer["id"], region["id"], code, eq_type, weight),
            )

        operator = conn.execute(
            "SELECT id FROM users WHERE email = 'operador@somple.com'"
        ).fetchone()

        operations = [
            ("EQ-001", "colheita", "field", "Talhão Norte"),
            ("EQ-002", "pulverizacao", "field", "Talhão Leste"),
            ("EQ-003", "plantio", "field", "Talhão Sul"),
            ("EQ-004", "colheita", "near_water", "Talhão Norte"),
            ("EQ-005", "plantio", "field", "Talhão Leste"),
            ("EQ-006", "transporte", "transport", "Talhão Sul"),
        ]

        for code, op_type, category, region_name in operations:
            eq = conn.execute(
                """
                SELECT e.id FROM equipment e
                JOIN customers c ON c.id = e.customer_id
                WHERE c.external_code = 'DEMO-001' AND e.external_code = %s
                """,
                (code,),
            ).fetchone()
            region = conn.execute(
                "SELECT id FROM regions WHERE customer_id = %s AND name = %s",
                (customer["id"], region_name),
            ).fetchone()
            exists = conn.execute(
                """
                SELECT id FROM operations
                WHERE equipment_id = %s AND operation_type = %s AND status = 'running'
                LIMIT 1
                """,
                (eq["id"], op_type),
            ).fetchone()
            if exists:
                continue
            conn.execute(
                """
                INSERT INTO operations (
                    equipment_id, region_id, operator_user_id,
                    operation_category, operation_type, status, started_at
                )
                VALUES (%s, %s, %s, %s, %s, 'running', %s)
                """,
                (eq["id"], region["id"], operator["id"], category, op_type, now),
            )
            conn.execute(
                """
                INSERT INTO maintenance_records (equipment_id, performed_at, maintenance_type)
                SELECT %s, %s, 'preventiva'
                WHERE NOT EXISTS (
                    SELECT 1 FROM maintenance_records
                    WHERE equipment_id = %s AND maintenance_type = 'preventiva'
                )
                """,
                (eq["id"], now - timedelta(days=45), eq["id"]),
            )

        artifact = ARTIFACTS_DIR / f"{settings.model_name}-v1.0.0.joblib"
        metadata_path = ARTIFACTS_DIR / f"{settings.model_name}-v1.0.0.json"
        sha256 = None
        metrics = {}
        if artifact.exists():
            sha256 = hashlib.sha256(artifact.read_bytes()).hexdigest()
        if metadata_path.exists():
            metrics = json.loads(metadata_path.read_text(encoding="utf-8")).get("metrics", {})

        conn.execute(
            """
            INSERT INTO model_versions (
                model_name, version, artifact_uri, artifact_sha256,
                training_dataset_version, metrics, is_active
            )
            VALUES (%s, '1.0.0', %s, %s, 'sprint2-v1', %s::jsonb, TRUE)
            ON CONFLICT (model_name, version) DO UPDATE
            SET artifact_uri = EXCLUDED.artifact_uri,
                artifact_sha256 = EXCLUDED.artifact_sha256,
                metrics = EXCLUDED.metrics,
                is_active = TRUE
            """,
            (
                settings.model_name,
                str(artifact),
                sha256,
                json.dumps(metrics),
            ),
        )

    print("Demo data created.")
    print(f"Users password: {DEMO_PASSWORD}")


if __name__ == "__main__":
    init_database_pool()
    try:
        upsert_demo_data()
    finally:
        close_database_pool()
