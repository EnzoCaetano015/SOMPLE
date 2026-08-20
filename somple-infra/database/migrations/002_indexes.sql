BEGIN;

CREATE INDEX idx_regions_customer
    ON regions (customer_id);

CREATE INDEX idx_equipment_customer
    ON equipment (customer_id);

CREATE INDEX idx_equipment_region_status
    ON equipment (current_region_id, status);

CREATE INDEX idx_maintenance_equipment_date
    ON maintenance_records (equipment_id, performed_at DESC);

CREATE INDEX idx_incidents_equipment_date
    ON incidents (equipment_id, occurred_at DESC);

CREATE INDEX idx_operations_equipment_date
    ON operations (equipment_id, created_at DESC);

CREATE INDEX idx_operations_region_status
    ON operations (region_id, status);

CREATE INDEX idx_operations_category
    ON operations (operation_category);

CREATE INDEX idx_telemetry_operation_date
    ON telemetry_readings (operation_id, recorded_at DESC);

CREATE INDEX idx_telemetry_recorded_at
    ON telemetry_readings (recorded_at DESC);

CREATE INDEX idx_assessments_operation_date
    ON risk_assessments (operation_id, predicted_at DESC);

CREATE INDEX idx_assessments_level_date
    ON risk_assessments (risk_level, predicted_at DESC);

CREATE INDEX idx_alerts_status_date
    ON alerts (status, created_at DESC);

CREATE INDEX idx_alerts_severity_status
    ON alerts (severity, status);

CREATE INDEX idx_audit_logs_created_at
    ON audit_logs (created_at DESC);

CREATE INDEX idx_audit_logs_request_id
    ON audit_logs (request_id)
    WHERE request_id IS NOT NULL;

CREATE INDEX idx_audit_logs_entity
    ON audit_logs (entity_type, entity_id);

-- Ensures a single active version for each model name.
CREATE UNIQUE INDEX uq_model_versions_single_active
    ON model_versions (model_name)
    WHERE is_active = TRUE;

COMMIT;
