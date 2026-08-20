from contextlib import contextmanager
from typing import Generator

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from core.config import settings

_pool: ConnectionPool | None = None


def init_database_pool() -> None:
    global _pool
    if _pool is not None:
        return
    _pool = ConnectionPool(
        conninfo=settings.database_dsn,
        kwargs={
            "row_factory": dict_row,
            "connect_timeout": settings.db_connect_timeout_seconds,
        },
        min_size=1,
        max_size=10,
        open=True,
    )


def close_database_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def get_pool() -> ConnectionPool:
    if _pool is None:
        init_database_pool()
    assert _pool is not None
    return _pool


class Database:
    @staticmethod
    @contextmanager
    def session() -> Generator[Connection, None, None]:
        pool = get_pool()
        with pool.connection() as conn:
            yield conn

    @staticmethod
    @contextmanager
    def transaction() -> Generator[Connection, None, None]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.transaction():
                yield conn


def check_database_connection() -> bool:
    try:
        with Database.session() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False
