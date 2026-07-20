"""Tests for database configuration and connectivity."""

from sqlalchemy import text

from app.core.config import Settings
from app.db.session import build_engine, normalize_database_url


def test_sqlite_fallback_connects_without_external_services() -> None:
    settings = Settings(database_url="sqlite+pysqlite:///:memory:")
    engine = build_engine(settings)

    with engine.connect() as connection:
        value = connection.scalar(text("SELECT 1"))

    assert value == 1
    engine.dispose()


def test_postgresql_urls_select_psycopg_driver() -> None:
    assert normalize_database_url("postgres://host/db") == (
        "postgresql+psycopg://host/db"
    )
    assert normalize_database_url("postgresql://host/db") == (
        "postgresql+psycopg://host/db"
    )
