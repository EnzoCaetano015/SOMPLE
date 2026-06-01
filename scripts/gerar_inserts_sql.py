"""
Gera comandos INSERT a partir do dataset_sprint2.csv.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "data" / "dataset_sprint2.csv"
OUTPUT_PATH = BASE_DIR / "sql" / "inserts_sprint2.sql"

def esc(valor: str) -> str:
    return str(valor).replace("'", "''")

def main() -> None:
    df = pd.read_csv(DATASET_PATH)
    equipamentos = sorted(df["equipamento_id"].unique())

    linhas = ["-- Inserts gerados automaticamente para demonstração da Sprint 2\n"]
    for eq in equipamentos:
        peso_medio = round(df.loc[df["equipamento_id"] == eq, "peso_equipamento_t"].mean(), 2)
        linhas.append(
            f"INSERT INTO equipamento (id_equipamento, tipo, peso_base_t, status) "
            f"VALUES ('{eq}', 'maquina_agricola', {peso_medio}, 'ativo');"
        )

    linhas.append("\n")
    for _, r in df.iterrows():
        linhas.append(
            "INSERT INTO leitura_operacional "
            "(id_registro, id_equipamento, regiao, chuva_mm, temperatura_c, umidade_solo, tipo_solo, "
            "inclinacao_graus, distancia_agua_m, tipo_operacao, peso_equipamento_t, dias_desde_manutencao, incidentes_previos) "
            f"VALUES ({int(r.id_registro)}, '{esc(r.equipamento_id)}', '{esc(r.regiao)}', {r.chuva_mm}, {r.temperatura_c}, "
            f"{r.umidade_solo}, '{esc(r.tipo_solo)}', {r.inclinacao_graus}, {r.distancia_agua_m}, "
            f"'{esc(r.tipo_operacao)}', {r.peso_equipamento_t}, {int(r.dias_desde_manutencao)}, {int(r.incidentes_previos)});"
        )
        linhas.append(
            "INSERT INTO previsao_risco "
            "(id_registro, score_risco, nivel_risco, alerta, recomendacao, modelo_utilizado) "
            f"VALUES ({int(r.id_registro)}, {r.score_risco}, '{esc(r.nivel_risco)}', "
            f"'{esc(r.alerta)}', '{esc(r.recomendacao)}', 'Regra simulada + RandomForestClassifier');"
        )

    OUTPUT_PATH.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Arquivo gerado: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
