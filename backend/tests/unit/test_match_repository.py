"""Match repository tests."""

from app.core.config import Settings
from app.db.base import Base
from app.db.session import build_engine, build_session_factory
from app.repositories.datasets import DatasetRepository
from app.repositories.matches import MatchRepository
from app.repositories.teams import TeamPlayerRepository


def test_match_repository_is_provider_idempotent() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        teams = TeamPlayerRepository(session)
        home = teams.get_or_create_team(
            source="synthetic", external_id="home", name="Home"
        )
        away = teams.get_or_create_team(
            source="synthetic", external_id="away", name="Away"
        )
        dataset = DatasetRepository(session).create_if_absent(
            provider="PlayerPulse",
            source_registry_id="synthetic_playerpulse",
            checksum="b" * 64,
            rights_snapshot={},
            manifest=[],
            is_synthetic=True,
        )
        values = {
            "source": "synthetic",
            "external_id": "match-1",
            "home_team_id": home.id,
            "away_team_id": away.id,
            "dataset_import_id": dataset.id,
            "is_synthetic": True,
        }
        repository = MatchRepository(session)

        first = repository.create_if_absent(**values)
        second = repository.create_if_absent(**values)

        assert first.id == second.id
        assert repository.get(first.id) is first
        assert repository.list() == [first]
    engine.dispose()
