# Modelo de dados SOMPLE — Sprint 3

```mermaid
erDiagram
    CUSTOMERS ||--o{ REGIONS : possui
    CUSTOMERS ||--o{ EQUIPMENT : possui
    REGIONS ||--o{ EQUIPMENT : localiza
    EQUIPMENT ||--o{ MAINTENANCE_RECORDS : recebe
    EQUIPMENT ||--o{ INCIDENTS : possui
    EQUIPMENT ||--o{ OPERATIONS : executa
    REGIONS ||--o{ OPERATIONS : ocorre_em
    USERS ||--o{ OPERATIONS : opera
    OPERATIONS ||--o{ TELEMETRY_READINGS : gera
    OPERATIONS ||--o{ RISK_ASSESSMENTS : avaliada_por
    TELEMETRY_READINGS ||--o{ RISK_ASSESSMENTS : alimenta
    MODEL_VERSIONS ||--o{ RISK_ASSESSMENTS : executa
    RISK_ASSESSMENTS ||--o{ RISK_FACTORS : explica
    RISK_ASSESSMENTS ||--o{ ALERTS : gera
    USERS ||--o{ ALERTS : reconhece
    USERS ||--o{ AUDIT_LOGS : executa

    CUSTOMERS {
        bigint id PK
        varchar external_code UK
        varchar name
    }

    REGIONS {
        bigint id PK
        bigint customer_id FK
        varchar name
        char state_code
    }

    EQUIPMENT {
        bigint id PK
        bigint customer_id FK
        bigint current_region_id FK
        varchar external_code
        varchar equipment_type
        numeric weight_tons
        varchar status
    }

    OPERATIONS {
        bigint id PK
        bigint equipment_id FK
        bigint region_id FK
        bigint operator_user_id FK
        varchar operation_category
        varchar operation_type
        varchar status
    }

    TELEMETRY_READINGS {
        bigint id PK
        bigint operation_id FK
        timestamptz recorded_at
        numeric rainfall_mm
        numeric temperature_c
        numeric soil_moisture_pct
        varchar soil_type
        numeric slope_degrees
        numeric distance_to_water_m
        jsonb raw_payload
    }

    MODEL_VERSIONS {
        bigint id PK
        varchar model_name
        varchar version
        text artifact_uri
        jsonb metrics
        boolean is_active
    }

    RISK_ASSESSMENTS {
        bigint id PK
        bigint operation_id FK
        bigint telemetry_reading_id FK
        bigint model_version_id FK
        smallint risk_score
        varchar risk_level
        numeric confidence
        jsonb input_snapshot
        jsonb output_snapshot
        timestamptz predicted_at
    }

    RISK_FACTORS {
        bigint id PK
        bigint assessment_id FK
        smallint rank
        varchar factor_code
        varchar factor_label
        numeric importance
        varchar direction
    }

    ALERTS {
        bigint id PK
        bigint assessment_id FK
        varchar severity
        varchar status
        text message
        text recommendation
    }

    AUDIT_LOGS {
        bigint id PK
        bigint actor_user_id FK
        varchar event_type
        varchar entity_type
        bigint entity_id
        varchar request_id
        jsonb metadata
        timestamptz created_at
    }
```

## Decisão de modelagem

O modelo é relacional porque o SOMPLE precisa consultar e auditar relações claras entre:

**cliente → região → equipamento → operação → telemetria → predição → alerta**.

`JSONB` é usado somente onde a flexibilidade é útil (`raw_payload`, snapshots e metadados), sem transformar o banco inteiro em armazenamento semi-estruturado.
