from psycopg import Connection


class AuthRepository:
    @staticmethod
    def find_user_by_email(conn: Connection, email: str) -> dict | None:
        row = conn.execute(
            """
            SELECT id, name, email, password_hash, role, is_active
            FROM users
            WHERE email = %s
            LIMIT 1
            """,
            (email,),
        ).fetchone()
        return row
