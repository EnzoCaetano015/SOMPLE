# Modelo 1.1.0

Treinamento executado sobre 180 registros com `StratifiedKFold(n_splits=2)` e previsões fora da amostra. O artefato final foi ajustado com todas as 180 linhas.

| Item | Resultado |
| --- | --- |
| Accuracy | 0,7667 |
| F1 macro | 0,5116 |
| MAE | 8,8325 |
| RMSE | 11,9401 |
| R² | 0,5945 |
| SHA-256 | `8ea7d658403aca46be7b6ef71f75fde9bd5077ed6d8ec97a847f569e960e0d67` |

O hash do arquivo foi comparado ao valor ativo em `model_versions`; ambos coincidiram. A versão `1.0.0` ficou inativa e a `1.1.0`, ativa. O runtime Docker foi reconstruído com scikit-learn 1.9.0 e carregou o artefato sem aviso de incompatibilidade.

Relatórios completos: `somple-backend/ml/training/reports/model-v1.1.0-evaluation.md` e `.json`.
