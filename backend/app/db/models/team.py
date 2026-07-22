"""Team persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.player import Player


class Team(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Provider-scoped football team identity."""

    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_teams_source_external_id"),
    )

    external_id: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    source: Mapped[str] = mapped_column(String(80), nullable=False)
    players: Mapped[list[Player]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )
