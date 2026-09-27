# Modelo de risco e decisão técnica

O Random Forest foi mantido por lidar bem com relações não lineares, combinar variáveis numéricas e categóricas após o pré-processamento e oferecer um baseline interpretável para o MVP sem introduzir uma troca de algoritmo sem evidência.

As dez features permanecem porque representam ambiente (`chuva_mm`, `temperatura_c`, `umidade_solo`, `tipo_solo`, `inclinacao_graus`, `distancia_agua_m`), operação (`tipo_operacao`) e contexto histórico do equipamento (`peso_equipamento_t`, `dias_desde_manutencao`, `incidentes_previos`). O dataset atual não oferece evidência suficiente para remover alguma delas.

A avaliação usa previsões fora da amostra com duas divisões estratificadas. Duas divisões são necessárias porque a classe `baixo` possui somente dois registros. O classificador é acompanhado por accuracy, precisão, recall e F1 macro/por classe e matriz de confusão; o regressor usa MAE, RMSE e R². O artefato final é treinado com os 180 registros após a avaliação.

Os dados são simulados, pequenos e fortemente desbalanceados. Portanto, as métricas demonstram reprodutibilidade acadêmica, não desempenho em produção. O uso real exigiria dados observados, validação temporal, monitoramento de drift e revisão atuarial/operacional.
