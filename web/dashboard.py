"""
Dashboard para demonstrar os alertas preventivos.

Execução:
streamlit run dashboard/dashboard_somple.py
"""

from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "data" / "dataset_sprint2.csv"

st.set_page_config(page_title="SOMPLE - Dashboard de Risco", layout="wide")
st.title("🚜 SOMPLE - Monitoramento de Risco Operacional")
st.caption("Sprint 2 | Score de risco, alertas preventivos e visão por equipamento/região")

if not DATASET_PATH.exists():
    st.error("Dataset da Sprint 2 não encontrado. Rode: python scripts/gerar_dataset_sprint2.py")
    st.stop()

df = pd.read_csv(DATASET_PATH)

col1, col2, col3 = st.columns(3)
with col1:
    equipamento = st.selectbox("Equipamento", ["Todos"] + sorted(df["equipamento_id"].unique().tolist()))
with col2:
    regiao = st.selectbox("Região", ["Todas"] + sorted(df["regiao"].unique().tolist()))
with col3:
    nivel = st.selectbox("Nível de risco", ["Todos"] + ["baixo", "medio", "alto", "critico"])

filtrado = df.copy()
if equipamento != "Todos":
    filtrado = filtrado[filtrado["equipamento_id"] == equipamento]
if regiao != "Todas":
    filtrado = filtrado[filtrado["regiao"] == regiao]
if nivel != "Todos":
    filtrado = filtrado[filtrado["nivel_risco"] == nivel]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Operações analisadas", len(filtrado))
m2.metric("Score médio", round(filtrado["score_risco"].mean(), 2) if len(filtrado) else 0)
m3.metric("Risco crítico", int((filtrado["nivel_risco"] == "critico").sum()))
m4.metric("Risco alto/crítico", int(filtrado["nivel_risco"].isin(["alto", "critico"]).sum()))

st.subheader("Distribuição de risco")
st.bar_chart(filtrado["nivel_risco"].value_counts())

st.subheader("Evolução do score por registro")
st.line_chart(filtrado.set_index("id_registro")["score_risco"])

st.subheader("Alertas preventivos")
colunas = [
    "id_registro", "equipamento_id", "regiao", "tipo_operacao", "score_risco",
    "nivel_risco", "distancia_agua_m", "umidade_solo", "alerta", "recomendacao"
]
st.dataframe(filtrado[colunas], use_container_width=True)
