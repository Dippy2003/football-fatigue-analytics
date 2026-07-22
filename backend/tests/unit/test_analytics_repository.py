"""Analytics repository tests."""

from typing import cast
from uuid import uuid4

from sqlalchemy import Table

from app.core.config import Settings
from app.db.base import Base
from app.db.models import PlayerMatchMetric, RiskAssessment
from app.db.session import build_engine, build_session_factory
from app.repositories.analytics import AnalyticsRepository


def test_analytics_repository_contract_uses_match_player_keys() -> None:
    table = cast(Table, PlayerMatchMetric.__table__)
    metric_unique = {constraint.name for constraint in table.constraints}
    risk_columns = RiskAssessment.__table__.columns

    assert "uq_metrics_match_player" in metric_unique
    assert "match_id" in risk_columns
    assert "player_id" in risk_columns


def test_latest_risk_returns_none_when_database_has_no_rows() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        assert (
            AnalyticsRepository(session).latest_risk(
                match_id=uuid4(), player_id=uuid4()
            )
            is None
        )
    engine.dispose()
