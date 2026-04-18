from sqlalchemy import text

from app.db.session import engine


def ensure_database_ready() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
