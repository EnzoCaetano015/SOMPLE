# SOMPLE — Sistema Inteligente de Predição de Riscos para Equipamentos Agrícolas

O **SOMPLE** é um protótipo desenvolvido para o Challenge da **Sompo Seguros na FIAP**. A solução cruza dados ambientais, operacionais e históricos para antecipar situações que podem causar danos ou perdas em equipamentos agrícolas.

A partir de uma telemetria, o sistema produz **score de risco de 0 a 100**, **nível de risco**, **confiança**, **fatores relevantes**, **recomendação preventiva** e, nos níveis alto ou crítico, um **alerta**. O resultado fica persistido e auditável, permitindo que operadores, gestores e seguradora atuem antes do incidente.

> Este README centraliza a documentação, a arquitetura e a validação final do projeto. Os READMEs internos são complementares.

## Sumário

- [Desafio](#desafio)
- [Objetivo da solução](#objetivo-da-solução)
- [Evolução do projeto](#evolução-do-projeto)
- [Arquitetura de software](#arquitetura-de-software)
- [Arquitetura do backend](#arquitetura-do-backend)
- [Módulos existentes](#módulos-existentes)
- [Fluxo de dados de ponta a ponta](#fluxo-de-dados-de-ponta-a-ponta)
- [Modelo de Inteligência Artificial](#modelo-de-inteligência-artificial)
- [Engenharia de dados e PostgreSQL](#engenharia-de-dados-e-postgresql)
- [Segurança da informação](#segurança-da-informação)
- [Dashboard](#dashboard)
- [Aderência às User Stories](#aderência-às-user-stories)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Executando localmente](#executando-localmente)
- [Como gerar um novo score de risco](#como-gerar-um-novo-score-de-risco)
- [Testes de regressão](#testes-de-regressão)
- [Implantação na AWS — bônus](#implantação-na-aws--bônus)
- [Evidências de execução](#evidências-de-execução)
- [Atendimento aos requisitos](#atendimento-aos-requisitos)
- [Decisões técnicas](#decisões-técnicas)
- [Limitações e próximos passos](#limitações-e-próximos-passos)
- [Checklist de entrega](#checklist-de-entrega)

## Desafio

O desafio proposto pela Sompo é identificar fatores ambientais e operacionais associados ao aumento do risco de danos, perdas, colisões, atolamentos, operações próximas à água, problemas durante transporte e outras situações relevantes no uso de equipamentos agrícolas.

```text
Abordagem tradicional: evento → dano → reação
SOMPLE:              dados → análise → previsão → alerta → prevenção
```

Chuva, umidade e tipo do solo, inclinação, proximidade de água, tipo de operação, peso do equipamento, manutenção e incidentes anteriores passam a compor uma avaliação rastreável, em vez de serem analisados isoladamente depois de um sinistro.

## Objetivo da solução

O SOMPLE integra telemetria, contexto ambiental, dados operacionais, histórico, PostgreSQL, modelo preditivo, API e dashboard. A solução oferece:

- ao **operador**, uma indicação objetiva do risco da operação;
- ao **gestor**, visão da frota, equipamentos prioritários, evolução e alertas;
- à **seguradora**, histórico rastreável para análise preventiva e governança da IA.

```text
Dados ambientais e operacionais
        ↓
Backend FastAPI e validação Pydantic
        ↓
PostgreSQL + Feature Builder
        ↓
Modelo de Machine Learning
        ↓
Score + classificação + confiança
        ↓
Fatores de risco + recomendação
        ↓
Alertas + auditoria
        ↓
Dashboard React
```

## Evolução do projeto

| Etapa | Objetivo | Resultado confirmado no histórico do repositório |
| --- | --- | --- |
| Sprint 1 | Estruturar problema, solução, personas, variáveis e arquitetura conceitual | Base conceitual, dataset inicial e regras de risco |
| Sprint 2 | Desenvolver dados, persistência SQL, modelo e primeira visualização | Dataset simulado, Random Forest Classifier, métricas e dashboard experimental em Streamlit |
| Sprint 3 | Integrar os componentes em um MVP funcional | FastAPI modular, PostgreSQL, pipeline transacional de inferência, JWT, auditoria, React integrado e Docker Compose |
| Consolidação final | Reforçar qualidade, confiabilidade e entrega | Idempotência, modelo v1.1.0, política única de risco, relatórios filtráveis, testes ampliados e evidências finais |

### Consolidação final

- domínios categóricos validados e duplicidade bloqueada pelo PostgreSQL;
- modelo `1.1.0` treinado por pipeline reproduzível, com validação dos dados e SHA-256;
- score, nível e alertas derivados de uma única política auditável;
- dashboard e relatórios com período, região e categoria de operação aplicados ao mesmo recorte;
- opções de filtro carregadas do banco, sem IDs de região hardcoded no dashboard;
- suíte de regressão ampliada, validação HTTP única e documentação final rastreável.

### O que mudou da Sprint 2 para a Sprint 3

| Sprint 2 | Sprint 3 |
| --- | --- |
| Modelo executado por script | Modelo versionado e carregado pelo backend |
| Dataset usado diretamente no treinamento e análise | Telemetria recebida pela API e contexto recuperado do PostgreSQL |
| Predição experimental | Predição acionada por endpoint autenticado |
| Saídas em arquivos e dashboard experimental | Telemetria, assessment, fatores e alertas persistidos |
| Execução manual do pipeline | Pipeline orquestrado por service em uma transação |
| Dashboard Streamlit da etapa experimental | Aplicação React + TypeScript consumindo a API |
| Análise pontual | Histórico de assessments e trilha de auditoria |
| Resultado técnico do modelo | Score, explicação, recomendação e alerta utilizáveis pela aplicação |

Principais evoluções da Sprint 3:

- backend FastAPI organizado por módulos e camadas;
- PostgreSQL com migrations, índices e views;
- integração do artefato de ML com o fluxo de telemetria;
- persistência de leituras, assessments, snapshots, fatores e alertas;
- recomendações e explicações dos fatores de risco;
- autenticação JWT, senha com Argon2 e endpoints protegidos;
- auditoria funcional de login, logout, telemetria, assessments e alertas;
- dashboard React integrado via Axios e TanStack React Query;
- ambiente local reproduzível com Docker Compose;
- preparação documental e técnica para uma futura implantação na AWS.

### Correções após o feedback da Sprint 3

- simulador de telemetria que autentica e envia leituras pelo endpoint real;
- RBAC aplicado no backend e refletido em menus, rotas e ações do frontend;
- tentativas inválidas de login persistidas como `auth.login.failed`;
- regressão automatizada para autenticação, autorização, telemetria e simulador;
- seis evidências funcionais reais e reproduzíveis, sem depender do vídeo.

## Arquitetura de software

```text
SOMPLE/
├── somple-frontend/
│   ├── src/api/                 # rotas, contratos e controllers HTTP
│   ├── src/components/          # componentes reutilizáveis
│   ├── src/pages/               # telas e estados da interface
│   └── src/router/              # rotas públicas e protegidas
├── somple-backend/
│   ├── api/v1/                  # composição das rotas versionadas
│   ├── core/                    # configuração, banco, JWT e observabilidade
│   ├── ml/                      # features, runtime, explicação e treinamento
│   ├── modules/                 # módulos funcionais da API
│   ├── scripts/                 # carga demo e simulador HTTP de telemetria
│   ├── utils/                   # erros, datas e regras compartilhadas
│   └── main.py                  # inicialização do FastAPI
├── somple-infra/
│   ├── database/                # migrations, seed e documentação do modelo
│   ├── docker/                  # imagens do backend, frontend e proxy
│   ├── aws/                     # arquitetura-alvo de nuvem
│   ├── docker-compose.yml       # ambiente local
│   └── docker-compose.aws.yml   # backend/proxy preparado para EC2
├── .env.example
└── README.md
```

| Responsabilidade | Camada |
| --- | --- |
| Apresentação e interação | `somple-frontend` |
| API e regras de negócio | `somple-backend/modules` |
| Persistência e consultas | repositories + PostgreSQL |
| Inteligência artificial | `somple-backend/ml` |
| Containers, banco e referência cloud | `somple-infra` |

A arquitetura AWS é uma evolução adicional de implantação e não substitui essa arquitetura de software.

## Arquitetura do backend

Cada módulo funcional segue o fluxo predominante:

```text
Router → Service → Repository → PostgreSQL
```

### Router

Define endpoints, parâmetros, schemas de entrada e saída e dependências de autenticação. A validação estrutural ocorre automaticamente com Pydantic.

### Service

Concentra regras de negócio e orquestra transações. No módulo de telemetria, coordena persistência, montagem de features, inferência, explicação, recomendação, alerta e auditoria.

### Repository

Executa consultas, inserções e atualizações no PostgreSQL, sem concentrar regras de apresentação.

| Pasta | Responsabilidade |
| --- | --- |
| `api` | Agregar os routers sob `/api/v1` |
| `core` | Configurações, pool do banco, segurança, autorização e logs HTTP |
| `modules` | Separar recursos e regras por domínio funcional |
| `ml` | Treinamento, artefato, runtime, Feature Builder, explicação e recomendações |
| `scripts` | Preparar dados do ambiente de demonstração |
| `utils` | Exceções, datas e classificação compartilhada de risco |

## Módulos existentes

| Módulo | Responsabilidade confirmada |
| --- | --- |
| Health | Healthcheck simples e readiness do banco/modelo |
| Auth | Login, emissão de JWT e logout auditado |
| Dashboard | KPIs, score da frota, ranking, evolução, distribuição e alertas recentes |
| Monitoring | Estado mais recente dos equipamentos e telemetrias, com filtros |
| Equipment | Listagem e detalhe de equipamentos e avaliações recentes |
| Operations | Consulta das operações e seus indicadores de risco |
| Telemetry | Ingestão e execução do pipeline completo de avaliação |
| Assessment | Detalhe de score, modelo, entradas, fatores e recomendação |
| Alerts | Listagem e atualização de status de alertas |
| Audit | Histórico filtrável de avaliações e consulta RBAC aos eventos de auditoria |

## Fluxo de dados de ponta a ponta

1. O cliente envia `POST /api/v1/telemetry` com Bearer Token.
2. FastAPI e Pydantic validam o corpo e seus limites.
3. O service confirma que a operação existe.
4. A leitura é persistida em `telemetry_readings`.
5. O `FeatureBuilder` combina telemetria com operação, equipamento, última manutenção e incidentes anteriores.
6. O runtime carrega o `.joblib` e executa classificador e regressor.
7. O sistema calcula nível, score e confiança.
8. O explainer identifica até cinco fatores e gera uma recomendação.
9. Assessment, snapshots e fatores são persistidos.
10. Riscos `high` ou `critical` geram alerta.
11. Eventos funcionais são gravados em `audit_logs`.
12. A transação é confirmada e IDs e resultado retornam ao cliente.
13. Dashboard e telas de detalhe consultam os dados pela API.

```mermaid
flowchart LR
    A[Telemetria] --> B[FastAPI + Pydantic]
    B --> C[Service]
    C --> D[(PostgreSQL)]
    D --> E[Feature Builder]
    E --> F[Classificador + Regressor]
    F --> G[Assessment]
    G --> H[Fatores + Recomendação]
    G --> I{Alto ou crítico?}
    I -->|Sim| J[Alerta]
    I -->|Não| K[Sem alerta]
    H --> D
    J --> D
    G --> L[Auditoria]
    L --> D
    D --> M[API de consulta]
    M --> N[Dashboard React]
```

## Modelo de Inteligência Artificial

O artefato final evolui o trabalho da Sprint 2 e está integrado ao backend como `somple-risk-classifier`, versão `1.1.0`:

- **Random Forest Classifier** classifica `low`, `medium`, `high` ou `critical`;
- **Random Forest Regressor** produz o score de 0 a 100.

O pipeline aplica `OneHotEncoder` às variáveis categóricas e serializa classificador, regressor e metadados em Joblib. O backend carrega esse artefato no runtime; não é necessário retreiná-lo para executar o MVP.

### Métricas registradas no artefato

| Métrica | Valor | Interpretação curta |
| --- | --- | --- |
| Accuracy | **76,67%** (`0.7667`) | Proporção de classes corretas nas previsões fora da amostra |
| Precisão macro | **0,5057** | Precisão média com o mesmo peso para cada classe |
| Recall macro | **0,5223** | Cobertura média com o mesmo peso para cada classe |
| F1 macro | **0,5116** | Equilíbrio entre precisão e recall das classes |
| MAE | **8,8325 pontos** | Erro absoluto médio do score |
| RMSE | **11,9401 pontos** | Erro quadrático com maior peso para desvios altos |
| R² | **0,5945** | Variação do score explicada pelo regressor |

As métricas vêm de `somple-backend/ml/artifacts/somple-risk-classifier-v1.1.0.json`, usando previsões fora da amostra em duas divisões estratificadas. O dataset acadêmico possui 180 registros simulados e apenas dois exemplos da classe baixa; os números não representam desempenho em produção.

### Dados utilizados pelo modelo

| Feature | Origem e significado |
| --- | --- |
| `chuva_mm` | Volume de chuva da telemetria |
| `temperatura_c` | Temperatura ambiente da telemetria |
| `umidade_solo` | Percentual de umidade do solo |
| `tipo_solo` | Característica categórica do terreno |
| `inclinacao_graus` | Inclinação do terreno |
| `distancia_agua_m` | Distância até corpo d'água |
| `tipo_operacao` | Atividade registrada na operação |
| `peso_equipamento_t` | Peso cadastrado do equipamento |
| `dias_desde_manutencao` | Dias desde a manutenção mais recente; usa 365 sem registro |
| `incidentes_previos` | Incidentes do equipamento anteriores à leitura |

O `Explainer` tenta usar SHAP e possui fallback baseado na importância das features. Os fatores são explicações do modelo, não novas medições.

### Treinamento opcional

```bash
cd somple-infra
docker compose --env-file ../.env exec backend python -m ml.training.train_model
```

O treinamento gera artefato, metadata SHA-256 e relatórios em `ml/training/reports`. A decisão técnica e as limitações estão em [`docs/MODEL.md`](docs/MODEL.md).

## Engenharia de dados e PostgreSQL

O PostgreSQL é a fonte persistente da aplicação.

| Grupo | Entidades |
| --- | --- |
| Identidade e organização | `users`, `customers`, `regions` |
| Contexto operacional | `equipment`, `maintenance_records`, `incidents`, `operations` |
| Entrada | `telemetry_readings` |
| IA | `model_versions`, `risk_assessments`, `risk_factors` |
| Ação e governança | `alerts`, `audit_logs` |

```mermaid
flowchart TD
    E[equipment] --> O[operations]
    O --> T[telemetry_readings]
    T --> R[risk_assessments]
    R --> F[risk_factors]
    R --> A[alerts]
    M[model_versions] --> R
    U[users] --> L[audit_logs]
```

- `input_snapshot` preserva o vetor exato enviado ao modelo.
- `output_snapshot` guarda probabilidades e métodos de score/explicação.
- `model_version_id` relaciona a decisão ao artefato ativo e às métricas.
- `audit_logs` registra ator, evento, entidade, request ID, endpoint, método, status e metadados.

Isso permite reconstruir uma inferência e trata auditoria como governança da IA, não apenas log técnico.

As migrations em `somple-infra/database/migrations` são montadas em `/docker-entrypoint-initdb.d` e executadas automaticamente pelo PostgreSQL **somente na criação de um volume vazio**.

## Segurança da informação

| Mecanismo | Estado e finalidade |
| --- | --- |
| JWT + Bearer Token | Implementado; autentica chamadas e expira conforme `JWT_EXP_HOURS` |
| Argon2 | Implementado; armazena hash, nunca senha em texto puro no banco |
| Endpoints protegidos | Implementado para todos os módulos, exceto health e login |
| Perfis no token | `admin`, `analyst` e `operator` são persistidos e incluídos no JWT |
| Autorização por perfil | Implementada com `require_roles` nos routers e UX equivalente no frontend |
| CORS | Configurável por `CORS_ORIGINS` |
| Variáveis de ambiente | Configuração e segredos ficam fora do código; somente exemplos são versionados |
| Auditoria | Login válido/inválido, logout, telemetria, assessment e eventos de alerta possuem registro |

```text
Usuário autenticado → JWT → endpoint protegido → operação → audit_logs
```

Logins inválidos retornam sempre `Invalid credentials` e geram `auth.login.failed` sem senha,
hash, token ou indicação da causa real. Requisições sem autenticação retornam `401`; uma role
autenticada sem permissão recebe `403` sem perder a sessão. O logout é auditado, mas não revoga o
token no servidor; o frontend remove o token local. Não use credenciais acadêmicas ou valores do
`.env.example` em produção.

### Matriz de permissões

| Recurso | admin | analyst | operator |
| --- | :---: | :---: | :---: |
| Dashboard, equipamentos, operações e monitoramento | sim | sim | sim |
| Leitura de alertas | sim | sim | sim |
| Alteração de status de alertas | sim | sim | não |
| Assessments | sim | sim | não |
| Auditoria | sim | sim | não |
| Envio de telemetria | sim | não | sim |

## Dashboard

O frontend usa **React 19**, **TypeScript**, **Vite**, **TanStack React Query**, **Axios**, **React Router**, **Recharts**, **Tailwind CSS** e componentes baseados em **shadcn/Base UI**.

Ele consome exclusivamente a API configurada em `VITE_API_BASE_URL`; não acessa o PostgreSQL diretamente. O Axios envia o Bearer Token e redireciona respostas `401` para o login.

Recursos confirmados:

- login e rotas autenticadas;
- KPIs, score geral, ranking, evolução e distribuição do risco e alertas recentes;
- monitoramento com resumo, tabela e filtros;
- lista e detalhe de equipamentos;
- operações, central de alertas e histórico de auditoria;
- detalhe do assessment com entradas, fatores e recomendação.

O React atende à apresentação dos resultados e mantém interface, backend Python e IA desacoplados.
A auditoria possui abas para assessments e eventos do sistema; esta última é restrita a `admin` e
`analyst` e pode filtrar eventos como `auth.login.failed`.

## Aderência às User Stories

| Necessidade da Sompo | Implementação | Situação |
| --- | --- | --- |
| Score por equipamento/operação | Assessments, APIs e dashboard | Implementado no MVP |
| Fatores ambientais e operacionais | Feature Builder + modelo + Risk Factors | Implementado no MVP |
| Alertas preventivos | Alerta automático em risco alto/crítico | Implementado no MVP |
| Recomendações | Recomendação associada ao assessment/alerta | Implementado no MVP |
| Explicabilidade | SHAP/fallback e fatores persistidos | Implementado no MVP |
| Histórico | PostgreSQL e telas de detalhe/auditoria | Implementado no MVP |
| Auditoria | `audit_logs` e snapshots | Implementado no MVP |
| Entrada de telemetria | `POST /api/v1/telemetry` | Implementado no MVP |
| Visualização | Dashboard React integrado | Implementado no MVP |
| Restrições por perfil | RBAC no backend e interface adaptada por role | Implementado |
| Fontes reais de clima/IoT | API aceita telemetria, sem integração externa | Parcialmente implementado no MVP |

## Tecnologias utilizadas

| Camada | Tecnologias confirmadas |
| --- | --- |
| Backend | Python 3.12, FastAPI, Pydantic, Uvicorn, psycopg |
| IA | Pandas, NumPy, Scikit-learn, Joblib, SHAP |
| Banco | PostgreSQL 16, SQL e JSONB |
| Frontend | React 19, TypeScript, Vite, React Query, Axios, React Router |
| Visualização | Recharts |
| Interface | Tailwind CSS, shadcn, Base UI, Lucide React |
| Infraestrutura local | Docker, Docker Compose, Nginx |
| Segurança | PyJWT, Argon2, Bearer Token, CORS |
| Cloud planejada | AWS EC2, RDS, S3, CloudFront e CloudWatch |

## Executando localmente

### Pré-requisitos

- [Git](https://git-scm.com/downloads);
- [Docker Desktop](https://www.docker.com/products/docker-desktop/), com Docker Engine e Compose.

No Windows, inicie o Docker Desktop e aguarde o engine ficar disponível.

### 1. Clone o repositório

```bash
git clone https://github.com/EnzoCaetano015/SOMPLE.git
cd SOMPLE
```

### 2. Configure o ambiente

O Compose local usa o `.env.example` da **raiz**.

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Antes de um ambiente compartilhado, altere pelo menos `POSTGRES_PASSWORD` e `JWT_SECRET_KEY`. Não versione `.env`.

### 3. Suba os containers

```bash
cd somple-infra
docker compose --env-file ../.env up -d --build
```

- `--env-file ../.env`: carrega as variáveis da raiz;
- `up`: cria e inicia os serviços;
- `-d`: executa em segundo plano;
- `--build`: reconstrói as imagens.

```bash
docker compose --env-file ../.env ps
```

Os containers são `somple-db`, `somple-backend` e `somple-frontend`.

### 4. Carregando os dados de demonstração

```bash
docker compose --env-file ../.env exec backend python -m scripts.create_demo_data
```

O comando executa `create_demo_data.py` como módulo Python a partir do diretório `/app` do container backend. O script cria/atualiza uma fazenda, três regiões, três usuários, seis equipamentos, seis operações, manutenções preventivas e a versão ativa do modelo. Ele não cria telemetrias ou assessments; esses dados surgem pelo endpoint de telemetria.

### Credenciais de demonstração

| Perfil | Usuário | Senha acadêmica |
| --- | --- | --- |
| Administrador | `admin@somple.com` | `Somple@123` |
| Analista | `analista@somple.com` | `Somple@123` |
| Operador | `operador@somple.com` | `Somple@123` |

> **Atenção:** credenciais exclusivas do ambiente acadêmico/de demonstração. Não reutilize em produção.

### 5. Gere telemetria pelo pipeline real

```bash
docker compose --env-file ../.env exec backend \
  python -m scripts.simulate_telemetry --scenario normal --count 10 --interval 1
```

Para gerar condições intermediárias ou com maior chance de risco:

```bash
docker compose --env-file ../.env exec backend \
  python -m scripts.simulate_telemetry --scenario moderate --count 5 --interval 1
docker compose --env-file ../.env exec backend \
  python -m scripts.simulate_telemetry --scenario critical --count 5 --interval 1
```

O script autentica como operador, obtém o JWT, descobre operações ativas e usa somente
`POST /api/v1/telemetry`. `--continuous` mantém o envio até `Ctrl+C`; `--operation-id` seleciona
uma operação conhecida. A URL e as credenciais podem ser sobrescritas por `SOMPLE_API_URL`,
`SOMPLE_DEMO_EMAIL` e `SOMPLE_DEMO_PASSWORD`.

### 6. Acesse os serviços

| Serviço | URL local |
| --- | --- |
| Frontend | `http://localhost:8080` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| OpenAPI JSON | `http://localhost:8000/openapi.json` |
| PostgreSQL | `localhost:5432` |

### 7. Valide a API e observe os resultados

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/ready
```

O primeiro retorna `{"status":"ok"}`. Quando banco e modelo estão disponíveis, o segundo informa `status: "ready"`, `database: "ok"`, `model: "ok"` e a versão.

## Como gerar um novo score de risco

O frontend apresenta os resultados, mas não possui formulário manual de telemetria. Execute o
simulador no container backend:

```bash
docker compose --env-file ../.env exec backend \
  python -m scripts.simulate_telemetry --scenario critical --count 1 --interval 0
```

O terminal informa IDs, score, nível de risco e alerta. Em seguida:

1. abra `http://localhost:8080` e faça login;
2. confira dashboard, monitoramento e alertas;
3. como `admin` ou `analyst`, abra o assessment para ver fatores e recomendação;
4. consulte o histórico de avaliações em `/audit`.

Os cenários são entradas plausíveis, não resultados forçados; a classificação continua sendo
determinada pelo modelo versionado.

## Testes de regressão

Suba o PostgreSQL temporário, instale as dependências de teste em uma `.venv` e execute:

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

A suíte recusa bancos cujo nome não contenha `test`. Ela cobre login, `401`/`403`, idempotência,
rollback, política de risco, integridade do modelo, filtros do dashboard, assessments, alertas,
auditoria e o simulador. No frontend, execute `vp check`, `vp test` e `vp run build`.

Com o ambiente completo em execução, valide o contrato público de ponta a ponta:

```bash
docker compose exec backend python -m scripts.validate_mvp
```

Em 26/09/2026, a validação final registrou `81 passed` no backend e 7 testes aprovados no
frontend. O check e o build foram concluídos; permaneceram quatro avisos preexistentes de Fast
Refresh e o aviso não bloqueante de tamanho do chunk principal.

### Parando o projeto

```bash
docker compose --env-file ../.env down
```

Executado em `somple-infra`, o comando preserva o volume do PostgreSQL.

### Reset completo do banco

> **Atenção:** remove o volume do PostgreSQL e apaga todos os dados locais.

```bash
docker compose --env-file ../.env down -v
docker compose --env-file ../.env up -d --build
docker compose --env-file ../.env exec backend python -m scripts.create_demo_data
```

No volume novo, o PostgreSQL executa automaticamente as migrations `001` a `006`. Em volume existente, aplique as migrations incrementais `005_telemetry_idempotency.sql` e `006_model_v1_1.sql`; migrations antigas não são reescritas.

## Implantação na AWS — bônus

> A AWS não é necessária para compreender a arquitetura principal do SOMPLE. A Sprint 3 incluiu, como evolução adicional, uma implantação acadêmica do MVP no AWS Academy Learner Lab.

É importante separar três conceitos:

- **arquitetura de software:** organização entre frontend, backend, persistência, IA e infraestrutura;
- **implantação realizada:** execução comprovada do MVP em uma instância Amazon EC2;
- **arquitetura cloud alvo:** evolução planejada com serviços gerenciados e distribuição adequada para um cenário mais próximo de produção.

### Implantação realizada na Sprint 3

Para validar que o MVP não depende exclusivamente do ambiente local, foi provisionada no AWS Academy uma instância Amazon EC2 denominada `somple-server`, do tipo `t2.medium`. As evidências registram a instância no estado `Executando`, associada a VPC, subnet, Security Group e IPv4 público.

A aplicação SOMPLE foi disponibilizada por esse endereço público: as rotas `/login` e `/dashboard` aparecem acessíveis pelo navegador, e o dashboard apresenta seis equipamentos monitorados.

```mermaid
flowchart LR
    U[Usuário] -->|HTTP + IPv4 público| EC2[EC2 somple-server]
    EC2 --> APP[Aplicação SOMPLE]
    APP --> LOGIN[Login]
    APP --> DASH[Dashboard]
```

O acesso demonstrado utiliza **HTTP diretamente pelo IPv4 público da EC2**, condição adequada ao laboratório acadêmico, mas não à publicação produtiva. O IPv4 do AWS Academy pode mudar quando a instância ou a sessão do laboratório for interrompida ou recriada; por isso, ele não é apresentado como URL permanente.

### Resultado da implantação

A execução em EC2 demonstrou que:

- a aplicação pode ser executada fora da máquina de desenvolvimento;
- a interface pode ser acessada externamente;
- a interface de autenticação e o dashboard estão disponíveis no ambiente publicado;
- a separação arquitetural entre frontend e backend é preservada pelo projeto;
- a configuração com containers favorece a portabilidade entre ambiente local e EC2.

Não foram realizados benchmarks nem medições de disponibilidade ou escalabilidade.


## Evidências de execução

As evidências reais da implantação estão organizadas em `docs/evidencias/aws`. Account ID e identificadores pessoais do AWS Academy foram ocultados antes da publicação; dados técnicos úteis à avaliação, como nome e tipo da instância, rede e IPv4 público, foram preservados.

### Evidências funcionais

As seis capturas pós-Sprint 3 ficam em `docs/evidencias/funcional`. O
[registro das evidências](docs/evidencias/funcional/README.md) documenta ambiente, comandos, cenário
e resultado observado para dashboard, monitoramento, assessment com explicabilidade, alerta crítico,
auditoria do pipeline e login inválido. Todos os PNGs foram capturados do sistema local em execução.

### Dashboard e filtros

As cinco capturas atuais em [`docs/evidencias/dashboard-relatorios`](docs/evidencias/dashboard-relatorios/)
registram os cenários normal, elevado, próximo à água, transporte e filtro pelo Talhão Norte.
As imagens foram produzidas pelo ambiente Docker isolado e mostram os filtros, KPIs, ranking e
relatório consolidado calculados pela API.

### Aplicação hospedada na AWS

<p align="center">
  <img src="docs/evidencias/aws/01-dashboard-aws.png" width="1000" alt="Dashboard do SOMPLE acessado pelo IPv4 público da EC2">
</p>

> **Figura 1 — Dashboard do SOMPLE executando em ambiente AWS através do IPv4 público da instância EC2, com seis equipamentos monitorados.**

<p align="center">
  <img src="docs/evidencias/aws/02-login-aws.png" width="1000" alt="Tela de login do SOMPLE hospedada na EC2">
</p>

> **Figura 2 — Tela de autenticação do SOMPLE disponibilizada pela instância AWS EC2.**

### Infraestrutura Amazon EC2

<p align="center">
  <img src="docs/evidencias/aws/04-ec2-instancia-executando.png" width="1000" alt="Instância somple-server em execução no Amazon EC2">
</p>

> **Figura 3 — Instância `somple-server`, do tipo `t2.medium`, em estado Executando no Amazon EC2.**

<p align="center">
  <img src="docs/evidencias/aws/03-ec2-conexao.png" width="1000" alt="Detalhes de conexão e rede da instância EC2 do SOMPLE">
</p>

> **Figura 4 — Página de conexão da instância EC2 utilizada pelo SOMPLE, exibindo estado, VPC, subnet, Security Group e IPv4 público.**

### Ambiente AWS Academy

<p align="center">
  <img src="docs/evidencias/aws/05-console-aws.png" width="900" alt="Console AWS do ambiente acadêmico usado pelo SOMPLE">
</p>

> **Figura 5 — Console AWS do ambiente acadêmico utilizado para a implantação do MVP SOMPLE.**

<p align="center">
  <img src="docs/evidencias/aws/06-aws-academy-lab.png" width="1000" alt="AWS Academy Learner Lab utilizado na Sprint 3">
</p>

> **Figura 6 — AWS Academy Learner Lab utilizado para provisionamento e execução da infraestrutura da Sprint 3.**

## Atendimento aos requisitos

| Requisito | Implementação | Evidência |
| --- | --- | --- |
| Arquitetura | Fluxo real e sequência em Mermaid | [`ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) |
| Exceções e qualidade | Erros controlados, domínios e rollback | [`qualidade-dados`](docs/evidencias/qualidade-dados/) |
| Duplicidades | Constraint incremental e resposta `409` | [`005_telemetry_idempotency.sql`](somple-infra/database/migrations/005_telemetry_idempotency.sql) |
| Modelo | Artefato v1.1.0, métricas e SHA-256 | [`modelo`](docs/evidencias/modelo/) |
| Score e alertas | Política `score-thresholds-v1` | [`score-alertas`](docs/evidencias/score-alertas/) |
| Integração | Telemetria até dashboard e auditoria | [`fluxo-ponta-a-ponta`](docs/evidencias/fluxo-ponta-a-ponta/) |
| Segurança e RBAC | JWT, Argon2, matriz e logs sanitizados | [`SECURITY.md`](docs/SECURITY.md) |
| Relatórios e filtros | Período, região e categoria no mesmo recorte | [`dashboard-relatorios`](docs/evidencias/dashboard-relatorios/) |
| Testes | Backend, frontend, build e validação HTTP | [`testes`](docs/evidencias/testes/) |
| Evidências | Pacote organizado e reproduzível | [`docs/evidencias`](docs/evidencias/) |
| Validação final | Classificação objetiva de todos os requisitos | [`VALIDATION.md`](docs/VALIDATION.md) |
| Vídeo | Roteiro pronto; link pendente de gravação humana | [`VIDEO.md`](docs/VIDEO.md) |

## Decisões técnicas

### FastAPI

Mantém backend e ML em Python, valida entradas com Pydantic e gera Swagger automaticamente.

### PostgreSQL

Oferece integridade relacional, histórico, auditoria, JSONB para snapshots e consultas analíticas.

### React

Separa apresentação das regras, permite componentes reutilizáveis e visualiza scores, fatores, gráficos e alertas. Atende ao requisito de interface; não é necessário substituí-lo por framework Python.

### Docker

Padroniza Python, Node/Nginx e PostgreSQL, reduz diferenças entre máquinas e simplifica a demonstração.

### Modelo no mesmo backend

Para o MVP, o runtime permanece no FastAPI. Um microsserviço separado adicionaria complexidade sem benefício proporcional ao escopo.

## Limitações e próximos passos

- Dados de treinamento e demonstração predominantemente simulados.
- Integrações diretas com IoT e APIs meteorológicas ainda não existem.
- O RBAC atual cobre os três perfis do MVP; novas roles exigirão ampliar a matriz e seus testes.
- O logout não possui blacklist/revogação de JWT no servidor.
- Alertas não disparam notificações externas.
- Drift, monitoramento e retreinamento não estão automatizados.
- A implantação acadêmica usa HTTP diretamente pelo IPv4 público da EC2.
- Georreferenciamento, tempo real e histórico real de sinistros podem ampliar o MVP.

## Checklist de entrega

- [x] Backend Python integrado
- [x] Banco PostgreSQL
- [x] Modelo de IA integrado
- [x] Pipeline de telemetria
- [x] Score e classificação
- [x] Fatores e recomendações
- [x] Alertas
- [x] Auditoria
- [x] Dashboard React
- [x] Docker Compose local
- [x] Documentação principal
- [x] Simulador de telemetria via API
- [x] Autorização específica por perfil
- [x] Auditoria de login inválido
- [x] Testes de regressão
- [x] Checklist de evidências funcionais reais
- [x] Implantação AWS Academy / EC2 documentada
- [x] Idempotência da telemetria
- [x] Modelo final v1.1.0 com integridade SHA-256
- [x] Política única de score, nível e alerta
- [x] Dashboard com filtros consistentes e relatório consolidado
- [x] Arquitetura e matriz de acesso consolidadas
- [ ] Vídeo final gravado e publicado

## Vídeo de demonstração

- Sprint 1 — [https://www.youtube.com/watch?v=04eJA7Vp_PU](https://www.youtube.com/watch?v=04eJA7Vp_PU)
- Sprint 2 — [https://www.youtube.com/watch?v=06a06tTTZ3s](https://www.youtube.com/watch?v=06a06tTTZ3s)
- Sprint 3 — [https://www.youtube.com/watch?v=YHfipkk08CA](https://www.youtube.com/watch?v=YHfipkk08CA)
- Vídeo final — **pendente de gravação**; roteiro em [`docs/VIDEO.md`](docs/VIDEO.md)
