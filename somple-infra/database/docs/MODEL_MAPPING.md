# Mapeamento do modelo Sprint 2 para o banco Sprint 3

O banco foi modelado para separar **dados de origem**, **dados operacionais** e **saídas da IA**.  
A predição não deve depender de um CSV no dashboard.

| Feature do modelo atual | Origem no banco | Regra |
|---|---|---|
| `chuva_mm` | `telemetry_readings.rainfall_mm` | leitura ambiental |
| `temperatura_c` | `telemetry_readings.temperature_c` | leitura ambiental |
| `umidade_solo` | `telemetry_readings.soil_moisture_pct` | leitura ambiental |
| `tipo_solo` | `telemetry_readings.soil_type` | contexto do terreno |
| `inclinacao_graus` | `telemetry_readings.slope_degrees` | contexto do terreno |
| `distancia_agua_m` | `telemetry_readings.distance_to_water_m` | contexto geográfico |
| `tipo_operacao` | `operations.operation_type` | atividade específica: plantio, colheita, transporte etc. |
| `peso_equipamento_t` | `equipment.weight_tons` | cadastro do equipamento |
| `dias_desde_manutencao` | `maintenance_records.performed_at` | calculado a partir da última manutenção anterior à predição |
| `incidentes_previos` | `incidents.occurred_at` | quantidade de incidentes do equipamento anteriores à predição |

## Saídas do modelo

Os campos antigos abaixo deixam de pertencer ao dataset operacional:

- `score_risco`
- `nivel_risco`
- `alerta`
- `recomendacao`

Eles passam a ser persistidos em:

- `risk_assessments`: score, nível, confiança, versão do modelo e snapshots;
- `risk_factors`: principais drivers/fatores de risco;
- `alerts`: alerta e recomendação.

## Por que existe `input_snapshot`

Antes de cada inferência, o backend monta o vetor final usado pelo pipeline e salva uma cópia imutável em `risk_assessments.input_snapshot`.

Exemplo:

```json
{
  "chuva_mm": 42.0,
  "temperatura_c": 31.4,
  "umidade_solo": 91.0,
  "tipo_solo": "argiloso",
  "inclinacao_graus": 14.0,
  "distancia_agua_m": 28.0,
  "tipo_operacao": "colheita",
  "peso_equipamento_t": 11.2,
  "dias_desde_manutencao": 84,
  "incidentes_previos": 2
}
```

Isso permite responder posteriormente:

1. quais dados foram usados;
2. qual versão do modelo executou a inferência;
3. qual resultado foi retornado;
4. quais fatores explicaram a decisão.

Essa é a base da trilha de auditoria exigida na Sprint 3.
