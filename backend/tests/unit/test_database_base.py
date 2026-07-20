"""Tests for shared SQLAlchemy model behavior."""

from datetime import UTC
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import Settings
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.session import build_engine, build_session_factory


class ExampleRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Test-only mapped entity."""

    __tablename__ = "example_records"

    label: Mapped[str] = mapped_column(String(50), nullable=False)


def test_shared_model_fields_use_uuid_and_utc() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        record = ExampleRecord(label="synthetic")
        session.add(record)
        session.flush()

        assert isinstance(record.id, UUID)
        assert record.created_at.tzinfo is UTC
        assert record.updated_at.tzinfo is UTC

    engine.dispose()
