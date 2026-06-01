"""
Treina e valida um modelo de Machine Learning para classificação de risco operacional.

Entradas:
- data/dataset_sprint2.csv

Saídas:
- outputs/txt/metricas_modelo.txt
- outputs/graficos/matrizes_confusao.png
- outputs/graficos/importancia_variaveis.png
- outputs/csv/correlacao_variaveis.csv
- outputs/csv/previsoes_risco.csv
- outputs/modelo_risco.joblib
"""

from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "data" / "dataset_sprint2.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
TXT_DIR = OUTPUT_DIR / "txt"
GRAFICOS_DIR = OUTPUT_DIR / "graficos"
CSV_DIR = OUTPUT_DIR / "csv"

OUTPUT_DIR.mkdir(exist_ok=True)
TXT_DIR.mkdir(exist_ok=True)
GRAFICOS_DIR.mkdir(exist_ok=True)
CSV_DIR.mkdir(exist_ok=True)

FEATURES = [
    "chuva_mm",
    "temperatura_c",
    "umidade_solo",
    "tipo_solo",
    "inclinacao_graus",
    "distancia_agua_m",
    "tipo_operacao",
    "peso_equipamento_t",
    "dias_desde_manutencao",
    "incidentes_previos",
]
TARGET = "nivel_risco"

ORDEM_RISCO = {"baixo": 0, "medio": 1, "alto": 2, "critico": 3}

def carregar_dados() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            "Dataset não encontrado. Rode primeiro: python scripts/gerar_dataset_sprint2.py"
        )
    return pd.read_csv(DATASET_PATH)

def main() -> None:
    df = carregar_dados()

    X = df[FEATURES]
    y = df[TARGET]

    colunas_categoricas = ["tipo_solo", "tipo_operacao"]
    colunas_numericas = [c for c in FEATURES if c not in colunas_categoricas]

    preprocessador = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), colunas_categoricas),
            ("num", "passthrough", colunas_numericas),
        ]
    )

    modelo = Pipeline(
        steps=[
            ("preprocessador", preprocessador),
            ("classificador", RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced")),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    acuracia = accuracy_score(y_test, y_pred)
    erro_medio_classe = mean_absolute_error(
        y_test.map(ORDEM_RISCO), pd.Series(y_pred).map(ORDEM_RISCO)
    )

    relatorio = classification_report(y_test, y_pred, zero_division=0)
    texto_metricas = f"""# Métricas do Modelo SOMPLE - Sprint 2

Acurácia: {acuracia:.4f}
Erro médio por classe ordinal: {erro_medio_classe:.4f}

Relatório de classificação:
{relatorio}

Interpretação:
- Acurácia mede o percentual de classificações corretas.
- Erro médio por classe ordinal mede o tamanho médio do erro entre níveis de risco.
  Exemplo: prever alto quando era crítico erra 1 nível; prever baixo quando era crítico erra 3 níveis.
"""
    (TXT_DIR / "metricas_modelo.txt").write_text(texto_metricas, encoding="utf-8")

    labels = ["baixo", "medio", "alto", "critico"]
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, labels=labels)
    plt.title("Matriz de Confusão - Modelo de Risco SOMPLE")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "matrizes_confusao.png", dpi=160)
    plt.close()

    # Importância das variáveis após OneHotEncoder
    feature_names = modelo.named_steps["preprocessador"].get_feature_names_out()
    importancias = modelo.named_steps["classificador"].feature_importances_
    df_importancias = pd.DataFrame({"variavel": feature_names, "importancia": importancias})
    df_importancias = df_importancias.sort_values("importancia", ascending=False).head(12)

    plt.figure(figsize=(10, 6))
    plt.barh(df_importancias["variavel"], df_importancias["importancia"])
    plt.gca().invert_yaxis()
    plt.title("Variáveis mais importantes para o risco")
    plt.xlabel("Importância")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "importancia_variaveis.png", dpi=160)
    plt.close()

    numericas = df.select_dtypes(include="number")
    numericas.corr(numeric_only=True).to_csv(CSV_DIR / "correlacao_variaveis.csv", encoding="utf-8")

    previsoes = X_test.copy()
    previsoes["risco_real"] = y_test.values
    previsoes["risco_previsto"] = y_pred
    previsoes.to_csv(CSV_DIR / "previsoes_risco.csv", index=False, encoding="utf-8")

    joblib.dump(modelo, OUTPUT_DIR / "modelo_risco.joblib")

    print(texto_metricas)
    print(f"Arquivos salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
