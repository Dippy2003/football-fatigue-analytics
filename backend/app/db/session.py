"""SQLAlchemy engine and session lifecycle."""

from collections.abc import Generator
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings, get_settings


def normalize_database_url(database_url: str) -> str:
    """Select psycopg explicitly for common PostgreSQL URL forms."""
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def build_engine(settings: Settings) -> Engine:
    """Build an engine with safe defaults for SQLite and PostgreSQL."""
    database_url = normalize_database_url(settings.database_url)
    connect_args: dict[str, Any] = {}
    engine_options: dict[str, Any] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        if database_url.endswith(":memory:"):
            engine_options["poolclass"] = StaticPool
    return create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        **engine_options,
    )


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create the transactional session factory."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


engine = build_engine(get_settings())
SessionLocal = build_session_factory(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a request-scoped session and always close it."""
    with SessionLocal() as session:
        yield session
