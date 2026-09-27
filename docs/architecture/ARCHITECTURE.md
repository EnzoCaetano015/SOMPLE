# Arquitetura do SOMPLE

## Componentes executados

```mermaid
flowchart LR
    U[Operador / Analista / Admin] --> R[React + TypeScript]
    S[Simulador HTTP / dispositivo] --> A
    R -->|JWT Bearer| A[FastAPI /api/v1]
    A --> P[Pydantic + RBAC + request ID]
    P --> SV[Services transacionais]
    SV --> RP[Repositories]
    RP --> DB[(PostgreSQL)]
    DB --> CTX[Operações, equipamento, manutenção e incidentes]
    CTX --> FB[FeatureBuilder]
    SV --> FB
    FB --> ML[Random Forest v1.1.0]
    ML --> EX[Explainer]
    EX --> RC[Recommendation]
    RC --> AS[Assessment + fatores]
    AS --> AL[Alerta alto/crítico]
    AS --> AU[Audit logs + snapshots]
    AL --> DB
    AU --> DB
    DB --> A
    A --> R
```

O frontend nunca acessa o PostgreSQL diretamente. Autenticação e autorização são aplicadas na API antes das operações protegidas.

## Sequência de inferência

```mermaid
sequenceDiagram
    participant C as Cliente autenticado
    participant API as FastAPI
    participant DB as PostgreSQL
    participant ML as Modelo v1.1.0

    C->>API: POST /telemetry
    API->>API: valida contrato e RBAC
    API->>DB: valida operação e modelo ativo
    API->>DB: insere telemetria (chave idempotente)
    API->>DB: consulta contexto histórico
    API->>ML: features + versão/SHA esperados
    ML-->>API: score + probabilidades
    API->>API: aplica política score-thresholds-v1
    API->>DB: assessment + snapshots + fatores
    alt score >= 50
        API->>DB: alerta e auditoria
    else score < 50
        API->>DB: auditoria sem alerta
    end
    API-->>C: 201 com assessment e alerta
```

## Implantação

O ambiente reproduzível usa Docker Compose com PostgreSQL 16, backend FastAPI e frontend servido por Nginx. A implantação AWS registrada anteriormente é acadêmica e usa HTTP; não representa uma topologia de produção. IoT, clima externo, mensageria e notificações não fazem parte da execução atual.
