from ml.schemas import FeatureVector


def build_recommendation(features: FeatureVector, factors: list[dict]) -> str:
    messages: list[str] = []

    if features.distancia_agua_m <= 30:
        messages.append("Utilizar rota alternativa afastada do corpo d'água.")
    if features.umidade_solo >= 85:
        messages.append("Avaliar adiamento da operação devido à umidade elevada do solo.")
    if features.inclinacao_graus >= 12:
        messages.append("Reduzir velocidade e avaliar rota alternativa em terreno inclinado.")
    if features.dias_desde_manutencao >= 90:
        messages.append("Encaminhar equipamento para inspeção preventiva.")
    if features.chuva_mm >= 35:
        messages.append("Monitorar condições pluviométricas e reduzir velocidade operacional.")

    if not messages:
        for factor in factors[:2]:
            code = factor.get("factor_code")
            if code == "incidentes_previos":
                messages.append("Reforçar protocolo operacional devido a incidentes anteriores.")
            elif code == "peso_equipamento_t":
                messages.append("Ajustar velocidade considerando o peso do equipamento.")

    if not messages:
        return "Manter monitoramento contínuo e seguir protocolo operacional padrão."

    return " ".join(messages)
