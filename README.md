# SOMPLE

Sistema de predição de riscos para equipamentos agrícolas, desenvolvido para o
Challenge Sompo Seguros na FIAP. Combina telemetria e contexto operacional para
calcular um score de 0 a 100, explicar fatores de risco e gerar alertas preventivos.

## Estrutura

- `somple-frontend/`: dashboard React, TypeScript e Vite+.
- `somple-backend/`: API FastAPI, autenticação JWT, auditoria e modelos de ML.
- `somple-infra/`: Docker Compose, Nginx, migrations e seeds PostgreSQL.

Fluxo: telemetria → API → PostgreSQL → modelo → avaliação/alerta → dashboard.
O modelo treinado está em `somple-backend/ml/artifacts/`.

## Execução local

Requisito: Docker com Docker Compose; no Windows, Docker Desktop em execução.
Na raiz do projeto, copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

No Linux/macOS, use `cp .env.example .env`.
Configure `POSTGRES_PASSWORD` e `JWT_SECRET_KEY` antes de compartilhar o ambiente.
Não versione o arquivo `.env`.

```sh
cd somple-infra
docker compose --env-file ../.env up -d --build
docker compose --env-file ../.env exec backend python -m scripts.create_demo_data
```

As migrations são aplicadas automaticamente na primeira criação do volume do banco.
O script de demonstração prepara usuários, equipamentos e operações; para gerar
avaliações e alertas, envie telemetria pelo simulador:

```sh
docker compose --env-file ../.env exec backend python -m scripts.simulate_telemetry --scenario normal --count 10 --interval 1
docker compose --env-file ../.env exec backend python -m scripts.simulate_telemetry --scenario critical --count 5 --interval 1
```

Cenários disponíveis: `normal`, `moderate` e `critical`.
O simulador autentica pela API e envia leituras para `POST /api/v1/telemetry`.

## Acesso

| Serviço | Endereço |
| --- | --- |
| Dashboard | http://localhost:8080 |
| API | http://localhost:8000/api/v1 |
| Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

Usuários de demonstração (senha comum: `Somple@123`):

- Administrador: `admin@somple.com`.
- Analista: `analista@somple.com`.
- Operador: `operador@somple.com`.

Use essas credenciais apenas no ambiente de demonstração.
Administrador e analista acessam assessments, auditoria e atualização de alertas.
Administrador e operador podem enviar telemetria.

## Verificação e testes

Com os serviços ativos, verifique a disponibilidade da API, do banco e do modelo:

```sh
curl http://localhost:8000/api/v1/health/ready
```

Para executar os testes do backend, use Python 3.12 e o banco temporário dedicado.
A partir da raiz, no PowerShell:

```powershell
cd somple-infra
docker compose -f docker-compose.test.yml up -d --wait
cd ../somple-backenda
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:TEST_DATABASE_URL="postgresql://somple_test:somple_test@localhost:5433/somple_test"
pytest -q
```

No Linux/macOS, ative `.venv/bin/activate` e defina `TEST_DATABASE_URL` com `export`.
Os testes exigem um banco cujo nome contenha `test`.

## Infraestrutura

- `somple-infra/docker-compose.yml`: frontend, backend e banco local.
- `somple-infra/docker-compose.test.yml`: PostgreSQL temporário para testes.
- `somple-infra/docker-compose.validation.yml`: configuração de validação do MVP.
- `somple-infra/docker-compose.aws.yml`: backend e proxy para EC2, com banco externo.

Para parar o ambiente local, execute em `somple-infra/`:

```sh
docker compose --env-file ../.env down
```
