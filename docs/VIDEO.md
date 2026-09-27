# Roteiro do vídeo final

## Preparação

```bash
docker compose -p somple-validation -f somple-infra/docker-compose.yml -f somple-infra/docker-compose.validation.yml up -d --build --wait
docker compose -p somple-validation -f somple-infra/docker-compose.yml -f somple-infra/docker-compose.validation.yml exec backend python -m scripts.create_demo_data
docker compose -p somple-validation -f somple-infra/docker-compose.yml -f somple-infra/docker-compose.validation.yml exec backend python -m scripts.validate_mvp
```

Essa composição usa volume e portas isolados, permitindo demonstrar a inicialização do zero sem apagar o banco local existente.

## Roteiro de até cinco minutos

- **0:00–0:30:** problema de perdas em equipamentos agrícolas e abordagem preventiva do SOMPLE.
- **0:30–1:10:** diagrama final: React, FastAPI, PostgreSQL, modelo e auditoria.
- **1:10–2:20:** login, envio real de telemetria e apresentação de score, nível e confiança.
- **2:20–3:10:** fatores, recomendação e alerta em cenário elevado/próximo à água.
- **3:10–4:10:** dashboard, evolução e filtros de região, Campo, Transporte e Próximo à água.
- **4:10–4:40:** versão/SHA do modelo, snapshots, request ID e RBAC.
- **4:40–5:00:** testes, validação final e limitações dos dados simulados.

## Checklist

- [ ] narração humana e duração máxima de cinco minutos;
- [ ] vídeo não listado;
- [ ] fluxo executado no sistema real;
- [ ] nenhuma senha, token ou secret visível;
- [ ] arquitetura, score, fatores, alerta, relatório e auditoria demonstrados;
- [ ] link inserido no README somente depois da publicação.

**Link do vídeo:** `PENDENTE — inserir após a gravação e publicação não listada.`
