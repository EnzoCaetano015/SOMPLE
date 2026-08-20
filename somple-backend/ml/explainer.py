from ml.schemas import FeatureVector, RiskPrediction

FACTOR_LABELS = {
    "chuva_mm": "Chuva acumulada",
    "temperatura_c": "Temperatura ambiente",
    "umidade_solo": "Umidade do solo",
    "tipo_solo": "Tipo de solo",
    "inclinacao_graus": "Inclinação do terreno",
    "distancia_agua_m": "Distância do corpo d'água",
    "tipo_operacao": "Tipo de operação",
    "peso_equipamento_t": "Peso do equipamento",
    "dias_desde_manutencao": "Dias desde manutenção",
    "incidentes_previos": "Incidentes anteriores",
}


class Explainer:
    @staticmethod
    def explain(
        pipeline,
        features: FeatureVector,
        prediction: RiskPrediction,
        *,
        top_k: int = 5,
    ) -> list[dict]:
        try:
            import pandas as pd
            import shap

            frame = pd.DataFrame([features.model_dump()])
            preprocessor = pipeline.named_steps["preprocessador"]
            classifier = pipeline.named_steps["classificador"]
            transformed = preprocessor.transform(frame)

            explainer = shap.TreeExplainer(classifier)
            shap_values = explainer.shap_values(transformed)

            class_index = list(classifier.classes_).index(
                _to_model_label(prediction.risk_level, classifier.classes_)
            )
            if isinstance(shap_values, list):
                values = shap_values[class_index][0]
            else:
                values = shap_values[0]

            feature_names = preprocessor.get_feature_names_out()
            pairs = sorted(
                zip(feature_names, values),
                key=lambda item: abs(item[1]),
                reverse=True,
            )[:top_k]

            explanation_method = "shap_local"
            factors = []
            for rank, (name, importance) in enumerate(pairs, start=1):
                code, label, value = _map_feature(name, features)
                factors.append(
                    {
                        "rank": rank,
                        "factor_code": code,
                        "factor_label": label,
                        "feature_name": code,
                        "feature_value": value,
                        "importance": min(1.0, abs(float(importance))),
                        "direction": "increase" if importance > 0 else "decrease",
                        "explanation_method": explanation_method,
                    }
                )
            return factors
        except Exception:
            return Explainer._global_fallback(pipeline, features)

    @staticmethod
    def _global_fallback(pipeline, features: FeatureVector) -> list[dict]:
        import pandas as pd

        frame = pd.DataFrame([features.model_dump()])
        classifier = pipeline.named_steps["classificador"]
        preprocessor = pipeline.named_steps["preprocessador"]
        importances = classifier.feature_importances_
        names = preprocessor.get_feature_names_out()
        pairs = sorted(zip(names, importances), key=lambda item: item[1], reverse=True)[:5]

        factors = []
        for rank, (name, importance) in enumerate(pairs, start=1):
            code, label, value = _map_feature(name, features)
            factors.append(
                {
                    "rank": rank,
                    "factor_code": code,
                    "factor_label": label,
                    "feature_name": code,
                    "feature_value": value,
                    "importance": float(importance),
                    "direction": "increase",
                    "explanation_method": "global_feature_importance",
                }
            )
        return factors


def _to_model_label(level: str, classes) -> str:
    reverse = {"low": "baixo", "medium": "medio", "high": "alto", "critical": "critico"}
    candidate = reverse.get(level, level)
    if candidate in classes:
        return candidate
    return level


def _map_feature(encoded_name: str, features: FeatureVector) -> tuple[str, str, object]:
    data = features.model_dump()
    for key in data:
        if key in encoded_name:
            return key, FACTOR_LABELS.get(key, key), data[key]
    return encoded_name, encoded_name, None
