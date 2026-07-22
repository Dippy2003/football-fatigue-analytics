"""Team and player repository operations."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Player, Team


class TeamPlayerRepository:
    """Provider-scoped team and player identity access."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_or_create_team(self, *, source: str, external_id: str, name: str) -> Team:
        team = self.session.scalar(
            select(Team).where(Team.source == source, Team.external_id == external_id)
        )
        if team is None:
            team = Team(source=source, external_id=external_id, name=name)
            self.session.add(team)
            self.session.flush()
        return team

    def get_or_create_player(
        self,
        *,
        team: Team,
        source: str,
        external_id: str,
        name: str,
        position: str | None = None,
    ) -> Player:
        player = self.session.scalar(
            select(Player).where(
                Player.source == source, Player.external_id == external_id
            )
        )
        if player is None:
            player = Player(
                team_id=team.id,
                source=source,
                external_id=external_id,
                name=name,
                position=position,
            )
            self.session.add(player)
            self.session.flush()
        return player

    def list_players_for_team(self, team_id: UUID) -> list[Player]:
        """Return players in stable external-ID order."""
        return list(
            self.session.scalars(
                select(Player)
                .where(Player.team_id == team_id)
                .order_by(Player.external_id)
            )
        )
