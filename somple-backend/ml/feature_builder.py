from datetime import datetime

from psycopg import Connection

from ml.schemas import FeatureVector


class FeatureBuilder:
    @staticmethod
    def build(
        conn: Connection,
        *,
        operation_id: int,
        telemetry: dict,
        recorded_at: datetime,
    ) -> FeatureVector:
        context = conn.execute(
            """
            SELECT
                o.operation_type,
                e.weight_tons,
                e.id AS equipment_id
            FROM operations o
            JOIN equipment e ON e.id = o.equipment_id
            WHERE o.id = %s
            LIMIT 1
            """,
            (operation_id,),
        ).fetchone()

        if context is None:
            raise ValueError(f"Operation {operation_id} not found")

        maintenance = conn.execute(
            """
            SELECT performed_at
            FROM maintenance_records
            WHERE equipment_id = %s AND performed_at <= %s
            ORDER BY performed_at DESC
            LIMIT 1
            """,
            (context["equipment_id"], recorded_at),
        ).fetchone()

        if maintenance:
            days_since = max(0, (recorded_at - maintenance["performed_at"]).days)
        else:
            days_since = 365

        incidents = conn.execute(
            """
            SELECT COUNT(*) AS total
            FROM incidents
            WHERE equipment_id = %s AND occurred_at <= %s
            """,
            (context["equipment_id"], recorded_at),
        ).fetchone()

        return FeatureVector(
            chuva_mm=float(telemetry["rainfall_mm"]),
            temperatura_c=float(telemetry["temperature_c"]),
            umidade_solo=float(telemetry["soil_moisture_pct"]),
            tipo_solo=str(telemetry["soil_type"]),
            inclinacao_graus=float(telemetry["slope_degrees"]),
            distancia_agua_m=float(telemetry["distance_to_water_m"]),
            tipo_operacao=str(context["operation_type"]),
            peso_equipamento_t=float(context["weight_tons"]),
            dias_desde_manutencao=int(days_since),
            incidentes_previos=int(incidents["total"] if incidents else 0),
        )
