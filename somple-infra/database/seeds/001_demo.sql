-- Optional development seed.
-- Run manually after the schema:
-- psql "$DATABASE_URL" -f somple-infra/database/seeds/001_demo.sql

BEGIN;

INSERT INTO customers (external_code, name)
VALUES ('DEMO-001', 'Fazenda Demonstração SOMPLE')
ON CONFLICT (external_code) DO NOTHING;

INSERT INTO regions (customer_id, name, state_code)
SELECT c.id, 'Talhão Norte', 'SP'
FROM customers c
WHERE c.external_code = 'DEMO-001'
ON CONFLICT (customer_id, name) DO NOTHING;

INSERT INTO regions (customer_id, name, state_code)
SELECT c.id, 'Talhão Leste', 'SP'
FROM customers c
WHERE c.external_code = 'DEMO-001'
ON CONFLICT (customer_id, name) DO NOTHING;

INSERT INTO equipment (
    customer_id,
    current_region_id,
    external_code,
    equipment_type,
    manufacturer,
    model,
    manufacture_year,
    weight_tons
)
SELECT
    c.id,
    r.id,
    'CL-310',
    'colheitadeira',
    'Demo',
    'CL-310',
    2023,
    11.20
FROM customers c
JOIN regions r ON r.customer_id = c.id AND r.name = 'Talhão Leste'
WHERE c.external_code = 'DEMO-001'
ON CONFLICT (customer_id, external_code) DO NOTHING;

INSERT INTO model_versions (
    model_name,
    version,
    artifact_uri,
    training_dataset_version,
    metrics,
    is_active
)
VALUES (
    'somple-risk-classifier',
    '1.0.0',
    'local://artifacts/modelo_risco.joblib',
    'sprint2-v1',
    '{"accuracy": 0.8444, "ordinal_mae": 0.1556}'::jsonb,
    TRUE
)
ON CONFLICT (model_name, version) DO NOTHING;

COMMIT;
