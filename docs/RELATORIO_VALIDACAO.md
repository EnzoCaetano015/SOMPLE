# Relatório de Validação Estatística - SOMPLE

## 1. Objetivo

Validar se o modelo preditivo consegue classificar corretamente o nível de risco operacional dos equipamentos agrícolas, considerando variáveis ambientais e operacionais.

## 2. User Story escolhida

Como **gestor de frota**, quero visualizar o risco de operação por equipamento e região para agir de forma preventiva antes que ocorram atolamentos, falhas mecânicas ou sinistros.

## 3. Variáveis utilizadas

| Variável | Papel na análise |
|---|---|
| chuva_mm | Indica condição climática recente. Chuva elevada aumenta risco de solo instável. |
| umidade_solo | Representa saturação do terreno. Quanto maior, maior o risco de atolamento. |
| tipo_solo | Solos argilosos tendem a reter mais água e elevar o risco. |
| inclinacao_graus | Declividades maiores aumentam risco de tombamento/deslizamento. |
| distancia_agua_m | Proximidade de rios/lagoas aumenta chance de solo encharcado. |
| tipo_operacao | Transporte e colheita expõem o equipamento a esforços diferentes. |
| peso_equipamento_t | Equipamentos mais pesados têm maior chance de afundamento. |
| dias_desde_manutencao | Manutenção atrasada aumenta risco operacional. |
| incidentes_previos | Histórico de problemas indica maior probabilidade de recorrência. |

## 4. Modelo escolhido

Foi utilizado o algoritmo **Random Forest Classifier**.

### Justificativa

A escolha é adequada porque:

- trabalha bem com variáveis numéricas e categóricas;
- é eficiente para classificação de risco;
- permite observar importância das variáveis;
- é mais robusto que uma árvore de decisão isolada;
- atende ao objetivo acadêmico de gerar classificação, score e alerta preventivo.

## 5. Métricas analisadas

As métricas geradas pelo script `scripts/modelo_risco.py` são:

- **Acurácia**: percentual de classificações corretas;
- **Matriz de confusão**: mostra acertos e erros por classe de risco;
- **Erro médio ordinal**: mede o tamanho médio do erro entre níveis de risco;
- **Importância das variáveis**: indica quais fatores mais influenciaram o modelo;
- **Correlação das variáveis**: ajuda a identificar relação estatística entre fatores ambientais e score de risco.

## 6. Interpretação esperada

Um bom resultado para esta Sprint não é “modelo perfeito”. O importante é provar que existe um fluxo funcional:

```text
Dataset simulado → tratamento → modelo preditivo → métricas → alerta preventivo → dashboard
```

## 7. Evidências para inserir no GitHub

Após executar o modelo, inserir prints dos seguintes arquivos:

- `outputs/metricas_modelo.txt`
- `outputs/matriz_confusao.png`
- `outputs/importancia_variaveis.png`
- dashboard executando no Streamlit
- consultas SQL rodadas no banco

## 8. Conclusão

A validação estatística permite demonstrar que o SOMPLE não apenas registra dados, mas transforma dados brutos em inteligência aplicada para prevenção de riscos agrícolas. Essa é a evolução central da Sprint 2.
