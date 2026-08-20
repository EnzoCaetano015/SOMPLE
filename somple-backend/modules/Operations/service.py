from core.database import Database
from modules.Operations.repository import OperationsRepository
from modules.Operations.schemas import OperationItem, OperationsResponse
from utils.risk import risk_level_from_score


class OperationsService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = OperationsRepository()

    def list_operations(self) -> OperationsResponse:
        rows = self._repository.fetch_grouped(self._conn)
        items = []
        for row in rows:
            avg_score = int(row["average_risk_score"] or 0)
            items.append(
                OperationItem(
                    key=f"{row['operation_type']}:{row['region_id']}",
                    name=row["operation_type"].capitalize(),
                    region_id=row["region_id"],
                    region_name=row["region_name"],
                    equipment_count=int(row["equipment_count"]),
                    average_risk_score=avg_score,
                    risk_level=risk_level_from_score(avg_score),
                    status=row["status"] or "planned",
                )
            )
        return OperationsResponse(items=items)


def list_operations() -> OperationsResponse:
    with Database.session() as conn:
        return OperationsService(conn).list_operations()
