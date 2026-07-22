"""Team/player repository tests."""

from app.core.config import Settings
from app.db.base import Base
from app.db.session import build_engine, build_session_factory
from app.repositories.teams import TeamPlayerRepository


def test_team_and_player_creation_is_idempotent() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        repository = TeamPlayerRepository(session)
        team = repository.get_or_create_team(
            source="synthetic_playerpulse", external_id="home", name="Synthetic Home"
        )
        duplicate = repository.get_or_create_team(
            source="synthetic_playerpulse", external_id="home", name="Ignored"
        )
        player = repository.get_or_create_player(
            team=team,
            source="synthetic_playerpulse",
            external_id="home-01",
            name="Synthetic Player 01",
        )

        assert duplicate.id == team.id
        assert repository.list_players_for_team(team.id) == [player]
    engine.dispose()
