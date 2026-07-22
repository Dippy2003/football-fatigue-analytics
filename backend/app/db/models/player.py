"""Player persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.team import Team


class Player(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """An anonymized or permissioned player identity."""

    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_players_source_external_id"),
        Index("ix_players_team_position", "team_id", "position"),
    )

    external_id: Mapped[str] = mapped_column(String(100), nullable=False)
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    position: Mapped[str | None] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(80), nullable=False)
    team: Mapped[Team] = relationship(back_populates="players")
