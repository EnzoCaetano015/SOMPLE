# Score, nível e alerta

Os testes de fronteira aprovaram os pontos 0, 24, 25, 49, 50, 74, 75 e 100. O nível é derivado exclusivamente do score e alertas são criados apenas para `high` e `critical`.

Na validação HTTP real foram enviados seis cenários. Todos produziram assessment, fatores e recomendação; os cenários elevados produziram alertas com título e mensagem em português. O `output_snapshot` registrou score, nível, confiança, probabilidades, método, thresholds e versão da política.

Comando executado:

```powershell
docker compose -p somple-validation -f somple-infra/docker-compose.yml -f somple-infra/docker-compose.validation.yml exec -T backend python -m scripts.validate_mvp
```
