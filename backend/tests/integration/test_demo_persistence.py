"""Stored demo integration tests."""

from sqlalchemy import func, select

from app.core.config import Settings
from app.db.base import Base
from app.db.models import DatasetImport, Match, Player, PlayerMatchMetric
from app.db.session import build_engine, build_session_factory
from app.services.demo import create_demo_dataset


def test_demo_persistence_is_complete_and_idempotent() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        first = create_demo_dataset(session, seed=42, period_duration_s=10)
        second = create_demo_dataset(session, seed=42, period_duration_s=10)

        assert first.created
        assert not second.created
        assert first.match.id == second.match.id
        assert session.scalar(select(func.count()).select_from(DatasetImport)) == 1
        assert session.scalar(select(func.count()).select_from(Match)) == 1
        assert session.scalar(select(func.count()).select_from(Player)) == 20
        assert session.scalar(select(func.count()).select_from(PlayerMatchMetric)) == 20
    engine.dispose()
