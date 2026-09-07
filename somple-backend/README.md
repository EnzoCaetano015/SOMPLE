# SOMPLE API

API de monitoramento e predição de riscos ambientais e operacionais para equipamentos agrícolas.

## Arquitetura

```text
Simulador -> HTTP API -> Telemetry -> PostgreSQL -> Feature Builder -> ML Runtime
-> Assessment -> Alert -> Audit -> Frontend (React Query)
```

Camadas por módulo: `router -> service -> repository`.

## Setup local

```bash
cd somple-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Suba o PostgreSQL pelo Docker Compose de `somple-infra`, execute as migrations e crie os dados demo:

```bash
python -m scripts.create_demo_data
uvicorn main:app --reload
```

Swagger: `http://localhost:8000/docs`.

## Simulador de telemetria

O simulador autentica pela API, encontra operações ativas e envia cada leitura somente por
`POST /api/v1/telemetry`. Assim, ele percorre o pipeline real e nunca grava diretamente no banco.

Pré-requisitos: API e PostgreSQL ativos e execução prévia de `scripts.create_demo_data`.

```bash
python -m scripts.simulate_telemetry --scenario normal --count 10 --interval 2
python -m scripts.simulate_telemetry --scenario moderate --count 5 --interval 1
python -m scripts.simulate_telemetry --scenario critical --interval 3 --continuous
```

- `normal`: condições ambientais estáveis;
- `moderate`: condições intermediárias;
- `critical`: valores plausíveis de chuva, umidade, inclinação e proximidade de água que aumentam a chance de risco;
- `--count`: número de leituras no modo finito;
- `--interval`: segundos entre leituras;
- `--continuous`: envia até receber `Ctrl+C`;
- `--operation-id`: usa uma operação específica em vez da descoberta automática.

Configuração opcional: `SOMPLE_API_URL`, `SOMPLE_DEMO_EMAIL` e `SOMPLE_DEMO_PASSWORD`.
Falhas de conexão, autenticação e respostas HTTP são resumidas no terminal sem expor tokens.

## Matriz RBAC

| Endpoint/grupo | admin | analyst | operator |
| --- | :---: | :---: | :---: |
| Health e login | público | público | público |
| Logout | sim | sim | sim |
| Dashboard | sim | sim | sim |
| Equipamentos | sim | sim | sim |
| Operações | sim | sim | sim |
| Monitoramento | sim | sim | sim |
| Leitura de alertas | sim | sim | sim |
| Alteração de status de alertas | sim | sim | não |
| Assessments | sim | sim | não |
| Auditoria | sim | sim | não |
| Envio de telemetria | sim | não | sim |

Ausência ou invalidade do token retorna `401`; usuário autenticado sem a role exigida recebe `403`.

## Testes

Os testes usam exclusivamente o PostgreSQL temporário `somple_test` na porta `5433`.

```powershell
cd somple-infra
docker compose -f docker-compose.test.yml up -d --wait
cd ..\somple-backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:TEST_DATABASE_URL="postgresql://somple_test:somple_test@localhost:5433/somple_test"
pytest -q
```

Linux/macOS usa o mesmo fluxo, ativando `.venv/bin/activate` e exportando `TEST_DATABASE_URL`.
A suíte recusa qualquer banco cujo nome não contenha `test`.

Execução confirmada em 07/09/2026: `53 passed`. A suíte cobre autenticação, eventos de login,
matriz RBAC, pipeline real, factors/recomendação, alertas, auditoria e contrato HTTP do simulador.

## Fluxo principal

1. `POST /api/v1/telemetry`;
2. persistência transacional de telemetria, assessment, factors, alert e audit;
3. consultas via `/dashboard`, `/monitoring`, `/equipment`, `/assessments/{id}` e `/audit`.

## Segurança e auditoria

Logins válidos geram `auth.login`. Usuário inexistente, inativo ou senha incorreta geram
`auth.login.failed` com mensagem externa única (`Invalid credentials`). O evento inclui contexto
HTTP e e-mail informado, mas nunca senha, hash, token ou a causa real da falha.

`GET /api/v1/audit/events` permite que `admin` e `analyst` consultem esses eventos e filtrem por
`event_type`; o endpoint mantém a mesma separação `router -> service -> repository` dos demais
módulos. Operadores recebem `403` e requisições sem autenticação recebem `401`.

## Deploy

O Dockerfile em `somple-infra/docker/backend/Dockerfile` executa:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Em produção AWS: FastAPI em EC2 (Docker), PostgreSQL em RDS privado, frontend em S3 + CloudFront.
Configure `CORS_ORIGINS` para o domínio do frontend.
