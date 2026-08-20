# SOMPLE API

API de monitoramento e predição de riscos ambientais e operacionais para equipamentos agrícolas.

## Arquitetura

```text
Telemetry -> FastAPI -> PostgreSQL -> Feature Builder -> ML Runtime
-> Assessment -> Alert -> Audit -> Frontend (React Query)
```

Camadas por módulo: `router -> service -> repository`.

## Setup local

```bash
cd somple-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Suba PostgreSQL (Docker Compose em `somple-infra`) e aplique migrations/seeds.

Treine o modelo:

```bash
python ml/training/train_model.py
python scripts/create_demo_data.py
```

Execute a API:

```bash
uvicorn main:app --reload
```

Swagger: `http://localhost:8000/docs`

## Variáveis de ambiente

Consulte [`.env.example`](.env.example).

## Fluxo principal

1. `POST /api/v1/telemetry`
2. Persistência transacional de telemetria, assessment, factors, alert e audit
3. Consultas via `/dashboard`, `/monitoring`, `/equipment`, `/assessments/{id}`, `/audit`

## Deploy

O Dockerfile em `somple-infra/docker/backend/Dockerfile` executa:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Em produção AWS: FastAPI em EC2 (Docker), PostgreSQL em RDS privado, frontend em S3 + CloudFront. Configure `CORS_ORIGINS` para o domínio do frontend.
