"""
Gera um dataset simulado mais completo para a Sprint 2.

O objetivo é representar cenários operacionais reais o suficiente para testar:
- persistência em banco SQL;
- análise estatística;
- treinamento de modelo preditivo;
- geração de score, alerta e recomendação preventiva.
"""

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

np.random.seed(42)

TIPOS_SOLO = ["argiloso", "arenoso", "siltoso", "misto"]
OPERACOES = ["colheita", "transporte", "pulverizacao", "plantio"]
REGIOES = ["Talhao Norte", "Talhao Sul", "Talhao Leste", "Talhao Oeste"]
EQUIPAMENTOS = ["TR-100", "TR-200", "CL-310", "PV-420", "PL-510"]

def classificar_score(linha: dict) -> int:
    score = 0

    # chuva e umidade aumentam chance de atolamento
    score += min(linha["chuva_mm"] * 1.2, 30)
    score += max(linha["umidade_solo"] - 35, 0) * 0.45

    # proximidade de água é crítica
    if linha["distancia_agua_m"] < 50:
        score += 28
    elif linha["distancia_agua_m"] < 200:
        score += 18
    elif linha["distancia_agua_m"] < 500:
        score += 8

    # declividade e peso aumentam risco mecânico/operacional
    score += linha["inclinacao_graus"] * 1.4
    score += max(linha["peso_equipamento_t"] - 5, 0) * 2.5

    # manutenção e histórico de incidente pesam bastante
    score += min(linha["dias_desde_manutencao"] / 8, 18)
    score += linha["incidentes_previos"] * 7

    if linha["tipo_solo"] == "argiloso":
        score += 10
    elif linha["tipo_solo"] == "siltoso":
        score += 6

    if linha["tipo_operacao"] == "transporte":
        score += 8
    elif linha["tipo_operacao"] == "colheita":
        score += 6

    return int(max(0, min(round(score), 100)))

def nivel(score: int) -> str:
    if score >= 75:
        return "critico"
    if score >= 55:
        return "alto"
    if score >= 30:
        return "medio"
    return "baixo"

def alerta(nivel_risco: str) -> str:
    return {
        "baixo": "Operação liberada com monitoramento padrão.",
        "medio": "Atenção: acompanhar clima e solo antes de continuar.",
        "alto": "Risco elevado: revisar rota, velocidade e condição do terreno.",
        "critico": "Operação não recomendada: adiar ou mudar rota imediatamente.",
    }[nivel_risco]

def recomendacao(nivel_risco: str) -> str:
    return {
        "baixo": "Manter operação planejada.",
        "medio": "Reduzir velocidade e verificar umidade do solo.",
        "alto": "Evitar áreas próximas à água e solicitar avaliação do gestor.",
        "critico": "Bloquear operação até melhora das condições ambientais.",
    }[nivel_risco]

def main() -> None:
    linhas = []

    for i in range(180):
        tipo_solo = np.random.choice(TIPOS_SOLO, p=[0.38, 0.27, 0.18, 0.17])
        chuva_mm = round(max(0, np.random.normal(22 if tipo_solo == "argiloso" else 14, 12)), 1)
        umidade_base = 42 + chuva_mm * 0.9
        if tipo_solo == "argiloso":
            umidade_base += 12
        umidade_solo = int(max(18, min(np.random.normal(umidade_base, 10), 98)))

        linha = {
            "id_registro": i + 1,
            "equipamento_id": np.random.choice(EQUIPAMENTOS),
            "regiao": np.random.choice(REGIOES),
            "chuva_mm": chuva_mm,
            "temperatura_c": round(np.random.normal(27, 4), 1),
            "umidade_solo": umidade_solo,
            "tipo_solo": tipo_solo,
            "inclinacao_graus": round(max(0, np.random.normal(8, 5)), 1),
            "distancia_agua_m": int(max(10, np.random.exponential(330))),
            "tipo_operacao": np.random.choice(OPERACOES, p=[0.35, 0.30, 0.20, 0.15]),
            "peso_equipamento_t": round(np.random.uniform(4.5, 12.5), 1),
            "dias_desde_manutencao": int(np.random.uniform(5, 180)),
            "incidentes_previos": int(np.random.choice([0, 1, 2, 3, 4], p=[0.48, 0.25, 0.15, 0.08, 0.04])),
        }
        linha["score_risco"] = classificar_score(linha)
        linha["nivel_risco"] = nivel(linha["score_risco"])
        linha["alerta"] = alerta(linha["nivel_risco"])
        linha["recomendacao"] = recomendacao(linha["nivel_risco"])
        linhas.append(linha)

    df = pd.DataFrame(linhas)
    saida = DATA_DIR / "dataset_sprint2.csv"
    df.to_csv(saida, index=False, encoding="utf-8")
    print(f"Dataset gerado: {saida}")
    print(df["nivel_risco"].value_counts())

if __name__ == "__main__":
    main()
