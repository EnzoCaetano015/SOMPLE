# SOMPLE Infra

Infraestrutura preparada para dois ambientes:

- **Local:** Docker Compose com React, FastAPI e PostgreSQL.
- **AWS:** React estático em S3/CloudFront, FastAPI em EC2 e PostgreSQL no RDS.

## Estrutura

```text
somple-infra/
├── docker/
│   ├── backend/Dockerfile
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── api-proxy/nginx.conf
├── database/
│   ├── migrations/
│   │   ├── 001_schema.sql
│   │   ├── 002_indexes.sql
│   │   └── 003_views.sql
│   ├── seeds/
│   │   └── 001_demo.sql
│   └── docs/
│       ├── ERD.md
│       └── MODEL_MAPPING.md
├── aws/
│   └── ARCHITECTURE.md
├── docker-compose.yml
├── docker-compose.aws.yml
└── .env.aws.example
```

## Ambiente local

Na raiz do repositório:

```bash
cp .env.example .env
cd somple-infra
docker compose --env-file ../.env up --build
```

Serviços:

- Frontend: `http://localhost:8080`
- FastAPI: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

As migrations SQL são executadas automaticamente somente quando o volume do PostgreSQL é criado pela primeira vez.

Para recriar o banco do zero durante desenvolvimento:

```bash
docker compose down -v
docker compose --env-file ../.env up --build
```

## Seed de demonstração

O seed não é carregado automaticamente.

```bash
psql "$DATABASE_URL" -f database/seeds/001_demo.sql
```

## Regra de segurança

Nunca versionar:

- `.env`;
- senha do RDS;
- `JWT_SECRET_KEY`;
- chaves AWS;
- certificados privados.

Versionar apenas os arquivos `*.example`.
