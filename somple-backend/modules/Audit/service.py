import json
from typing import Any

from fastapi import Request
from psycopg import Connection


class AuditRepository:
    @staticmethod
    def insert_log(
        conn: Connection,
        *,
        actor_user_id: int | None,
        event_type: str,
        entity_type: str | None,
        entity_id: int | None,
        request_id: str | None,
        endpoint: str | None,
        http_method: str | None,
        status_code: int | None,
        metadata: dict[str, Any],
    ) -> None:
        conn.execute(
            """
            INSERT INTO audit_logs (
                actor_user_id, event_type, entity_type, entity_id,
                request_id, endpoint, http_method, status_code, metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
            """,
            (
                actor_user_id,
                event_type,
                entity_type,
                entity_id,
                request_id,
                endpoint,
                http_method,
                status_code,
                json.dumps(metadata),
            ),
        )


class AuditService:
    def __init__(self, conn: Connection):
        self._conn = conn
        self._repository = AuditRepository()

    def log_event(
        self,
        *,
        event_type: str,
        request: Request | None = None,
        actor_user_id: int | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
        status_code: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        request_id = getattr(request.state, "request_id", None) if request else None
        endpoint = str(request.url.path) if request else None
        http_method = request.method if request else None

        if request is not None and hasattr(request.state, "principal"):
            actor_user_id = actor_user_id or request.state.principal.id

        self._repository.insert_log(
            self._conn,
            actor_user_id=actor_user_id,
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            request_id=request_id,
            endpoint=endpoint,
            http_method=http_method,
            status_code=status_code,
            metadata=metadata or {},
        )
