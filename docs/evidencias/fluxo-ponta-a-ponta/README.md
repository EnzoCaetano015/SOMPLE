# Fluxo ponta a ponta

Foi criada uma stack isolada com volume novo e portas alternativas usando `docker-compose.validation.yml`, sem apagar o banco de desenvolvimento existente.

Sequência executada:

1. build das imagens backend e frontend;
2. criação de volume PostgreSQL vazio;
3. aplicação automática das migrations 001 a 006;
4. carga demo;
5. health e readiness;
6. login administrativo;
7. envio de seis telemetrias cobrindo operações de campo, próxima à água e transporte;
8. consulta do dashboard e detalhe do último assessment.

Resultado final:

```text
PASS health
PASS readiness
PASS telemetry:normal
PASS telemetry:moderate
PASS telemetry:critical
PASS telemetry:critical
PASS telemetry:moderate
PASS telemetry:critical
PASS dashboard
PASS assessment
SOMPLE MVP validation completed successfully.
```

Containers da validação: `somple-validation-db`, `somple-validation-backend` e `somple-validation-frontend`, todos saudáveis durante a coleta.
