# SOMPLE

MVP para identificação de fatores ambientais e operacionais que elevam o risco de dano ou perda de equipamentos agrícolas.

## Arquitetura atual

```text
New-Somple/
├── somple-frontend/   # React + Vite + TypeScript
├── somple-backend/    # FastAPI
└── somple-infra/      # Docker, PostgreSQL e arquitetura AWS
```

## Infraestrutura

A infraestrutura foi preparada para:

- desenvolvimento local com Docker Compose;
- frontend React/Vite em S3 + CloudFront;
- API FastAPI em EC2;
- PostgreSQL em RDS;
- persistência de telemetria, avaliações de risco, alertas e auditoria.

Consulte:

- `somple-infra/README.md`
- `somple-infra/aws/ARCHITECTURE.md`
- `somple-infra/database/docs/ERD.md`
- `somple-infra/database/docs/MODEL_MAPPING.md`

## Estado

A arquitetura de frontend/backend está criada. A próxima etapa é implementar os módulos FastAPI e conectar as páginas React aos endpoints, utilizando o banco como fonte oficial dos dados exibidos.
