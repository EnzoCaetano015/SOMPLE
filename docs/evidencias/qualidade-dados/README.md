# Qualidade de dados e idempotência

Data: 26/09/2026. Ambiente: PostgreSQL 16 em Docker e backend em Python 3.14.7.

- `pytest tests/test_telemetry_pipeline.py tests/test_training_pipeline.py` integrou a suíte final de 81 testes aprovados.
- Payloads com `source` ou `soil_type` fora do domínio retornam `422`.
- A restrição `uq_telemetry_event` impede repetição de `operation_id + recorded_at + source`.
- A repetição retorna `409` sem expor detalhes do PostgreSQL, e os testes confirmam ausência de assessment, fatores, alerta e auditoria parciais.
- Falhas induzidas e ausência de modelo ativo exercitam rollback e retorno `503`.

Arquivos de prova: `somple-backend/tests/test_telemetry_pipeline.py`, `somple-backend/tests/test_training_pipeline.py` e migration `005_telemetry_idempotency.sql`.
