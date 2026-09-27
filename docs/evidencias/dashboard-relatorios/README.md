# Dashboard e relatórios

Inspeção visual real realizada em 27/09/2026 no ambiente Docker isolado,
em `http://localhost:18080/dashboard`, autenticada como administrador de demonstração.
O dashboard carregou sem overlay de erro e sem erros ou warnings no console do navegador.

## Execução

```powershell
docker compose -p somple-validation `
  -f somple-infra/docker-compose.yml `
  -f somple-infra/docker-compose.validation.yml up -d --build --wait

docker compose -p somple-validation `
  -f somple-infra/docker-compose.yml `
  -f somple-infra/docker-compose.validation.yml exec -T backend `
  python -m scripts.create_demo_data

docker compose -p somple-validation `
  -f somple-infra/docker-compose.yml `
  -f somple-infra/docker-compose.validation.yml exec -T backend `
  python -m scripts.simulate_telemetry --scenario normal `
  --operation-id 1 --count 1 --interval 0 --api-url http://backend:8000/api/v1
```

As demais capturas repetiram o simulador com os cenários `critical` ou `moderate`
para as operações 2, 4 e 6. As opções de categoria e região foram selecionadas
diretamente no dashboard após a persistência das leituras.

## Capturas

| Arquivo | Cenário e resultado observado |
| --- | --- |
| [`01-cenario-normal.png`](01-cenario-normal.png) | perfil `normal`, EQ-001, score 45 moderado, sem alerta |
| [`02-cenario-elevado.png`](02-cenario-elevado.png) | inclusão de perfil crítico, máximo 99, um equipamento em risco elevado e um alerta |
| [`03-proximo-a-agua.png`](03-proximo-a-agua.png) | categoria Próximo à água, EQ-004, score 99 crítico e um alerta |
| [`04-transporte.png`](04-transporte.png) | categoria Transporte, EQ-006, score 98 crítico e um alerta |
| [`05-filtro-regiao-talhao-norte.png`](05-filtro-regiao-talhao-norte.png) | região Talhão Norte, dois equipamentos, média 72, máximo 99 e um alerta |

Todas as imagens foram exportadas do sistema em execução no breakpoint desktop de
1440 x 1000. Nenhuma credencial, token ou segredo aparece nas capturas.
