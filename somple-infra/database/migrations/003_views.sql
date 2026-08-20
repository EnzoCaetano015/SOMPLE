BEGIN;

CREATE OR REPLACE VIEW v_latest_equipment_risk AS
SELECT DISTINCT ON (e.id)
    e.id AS equipment_id,
    e.external_code AS equipment_code,
    e.equipment_type,
    e.status AS equipment_status,
    c.id AS customer_id,
    c.name AS customer_name,
    r.id AS region_id,
    r.name AS region_name,
    o.id AS operation_id,
    o.operation_category,
    o.operation_type,
    ra.id AS assessment_id,
    ra.risk_score,
    ra.risk_level,
    ra.confidence,
    ra.predicted_at,
    mv.version AS model_version
FROM risk_assessments ra
JOIN operations o ON o.id = ra.operation_id
JOIN equipment e ON e.id = o.equipment_id
JOIN customers c ON c.id = e.customer_id
JOIN regions r ON r.id = o.region_id
JOIN model_versions mv ON mv.id = ra.model_version_id
ORDER BY e.id, ra.predicted_at DESC, ra.id DESC;

CREATE OR REPLACE VIEW v_active_alerts AS
SELECT
    a.id AS alert_id,
    a.severity,
    a.status,
    a.title,
    a.message,
    a.recommendation,
    a.created_at,
    ra.risk_score,
    ra.risk_level,
    ra.predicted_at,
    e.id AS equipment_id,
    e.external_code AS equipment_code,
    r.id AS region_id,
    r.name AS region_name,
    o.id AS operation_id,
    o.operation_category,
    o.operation_type
FROM alerts a
JOIN risk_assessments ra ON ra.id = a.assessment_id
JOIN operations o ON o.id = ra.operation_id
JOIN equipment e ON e.id = o.equipment_id
JOIN regions r ON r.id = o.region_id
WHERE a.status IN ('open', 'acknowledged');

COMMIT;
