BEGIN;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'uq_telemetry_event'
    ) THEN
        ALTER TABLE telemetry_readings
            ADD CONSTRAINT uq_telemetry_event
            UNIQUE (operation_id, recorded_at, source);
    END IF;
END $$;

COMMIT;
