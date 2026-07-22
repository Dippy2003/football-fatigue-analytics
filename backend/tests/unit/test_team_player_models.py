"""Team and player relationship tests."""

from typing import cast

from sqlalchemy import Table

from app.db.models import Player, Team


def test_team_and_player_use_provider_scoped_identity() -> None:
    team_table = cast(Table, Team.__table__)
    player_table = cast(Table, Player.__table__)
    team_constraints = {item.name for item in team_table.constraints}
    player_constraints = {item.name for item in player_table.constraints}

    assert "uq_teams_source_external_id" in team_constraints
    assert "uq_players_source_external_id" in player_constraints
    assert not Player.__table__.columns["team_id"].nullable
