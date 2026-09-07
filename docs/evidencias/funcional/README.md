# Evidências funcionais pós-Sprint 3

Capturas reais realizadas em **07/09/2026**, no ambiente local com Docker Desktop 29.7.2,
PostgreSQL 16, backend FastAPI e frontend Nginx exposto em `http://localhost:8080`.

## Preparação do cenário

Executado a partir da raiz do repositório:

```powershell
docker compose -f somple-infra/docker-compose.yml up -d --build --wait
docker compose -f somple-infra/docker-compose.yml exec -T backend python -m scripts.create_demo_data

cd somple-backend
.venv\Scripts\python.exe -m scripts.simulate_telemetry --scenario normal --count 6 --interval 0
.venv\Scripts\python.exe -m scripts.simulate_telemetry --scenario moderate --count 6 --interval 0
.venv\Scripts\python.exe -m scripts.simulate_telemetry --scenario critical --count 6 --interval 0
```

O produtor enviou 18 leituras exclusivamente por `POST /api/v1/telemetry`. O pipeline persistiu
18 assessments; nesta execução, os cenários `moderate` e `critical` produziram 12 alertas críticos.
Um alerta foi posteriormente reconhecido por analyst e resolvido por admin durante a validação RBAC.

Também foi enviada uma tentativa real de login com senha inválida e request ID
`evidencia-login-falho-20260907`. A resposta foi `401`, e a auditoria armazenou somente e-mail e
`reason: invalid_credentials`, sem senha, hash ou token.

## Capturas

1. [Dashboard populado](01-dashboard-populado.png): seis equipamentos, score da frota, ranking,
   distribuição, evolução e alertas recentes.
2. [Monitoramento de risco](02-monitoramento-risco.png): última telemetria de cada equipamento e
   classificação crítica gerada pelo modelo.
3. [Assessment com explicabilidade](03-assessment-shap.png): score, versão do modelo, fatores e
   recomendação preventiva do assessment 13.
4. [Alerta crítico](04-alerta-critico.png): alertas gerados pelo pipeline, com score e operação.
5. [Auditoria do fluxo](05-auditoria-fluxo.png): histórico real de assessments normais e críticos.
6. [Auditoria de login inválido](06-auditoria-login-falho.png): evento `auth.login.failed`, ator nulo,
   método, endpoint, request ID, status 401 e metadados sanitizados.

## Verificações complementares

- backend: `53 passed` com PostgreSQL dedicado `somple_test` na porta 5433;
- frontend: `vp check` sem erros, `vp test` com 3 testes e `vp run build` concluído;
- API: operador recebeu `403` em auditoria e alteração de alerta; analyst recebeu `403` no envio de
  telemetria e `200` na auditoria/alteração de alerta; admin recebeu `200` nas ações analíticas;
- navegador: operador não visualizou Histórico nem atalhos de assessment e foi redirecionado de
  `/audit` para `/dashboard`; analyst e admin acessaram a auditoria.

As imagens desta pasta são capturas do sistema em execução. Nenhum PNG foi fabricado ou usado como
placeholder.
