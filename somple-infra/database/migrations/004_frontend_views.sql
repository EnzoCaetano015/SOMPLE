BEGIN;

CREATE OR REPLACE VIEW v_latest_equipment_state AS
SELECT DISTINCT ON (e.id)
    e.id AS equipment_id,
    e.external_code AS equipment_code,
    e.equipment_type,
    e.status AS equipment_status,
    r.id AS region_id,
    r.name AS region_name,
    o.id AS operation_id,
    o.operation_type,
    o.operation_category,
    o.status AS operation_status,
    tr.id AS telemetry_reading_id,
    tr.speed_kmh,
    tr.soil_moisture_pct,
    tr.rainfall_mm,
    tr.recorded_at,
    ra.id AS assessment_id,
    ra.risk_score,
    ra.risk_level,
    ra.confidence,
    ra.predicted_at,
    mv.version AS model_version
FROM equipment e
LEFT JOIN operations o ON o.equipment_id = e.id
    AND o.status IN ('planned', 'running', 'paused')
LEFT JOIN LATERAL (
    SELECT tr.*
    FROM telemetry_readings tr
    WHERE tr.operation_id = o.id
    ORDER BY tr.recorded_at DESC, tr.id DESC
    LIMIT 1
) tr ON TRUE
LEFT JOIN LATERAL (
    SELECT ra.*
    FROM risk_assessments ra
    WHERE ra.operation_id = o.id
    ORDER BY ra.predicted_at DESC, ra.id DESC
    LIMIT 1
) ra ON TRUE
LEFT JOIN model_versions mv ON mv.id = ra.model_version_id
LEFT JOIN regions r ON r.id = o.region_id
ORDER BY e.id, o.created_at DESC NULLS LAST, ra.predicted_at DESC NULLS LAST;

CREATE INDEX IF NOT EXISTS idx_alerts_assessment_id ON alerts (assessment_id);
CREATE INDEX IF NOT EXISTS idx_risk_factors_assessment_id ON risk_factors (assessment_id);
CREATE INDEX IF NOT EXISTS idx_risk_assessments_telemetry_reading_id
    ON risk_assessments (telemetry_reading_id);

COMMIT;
