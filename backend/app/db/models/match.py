"""Football match persistence model."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Match(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Provider-scoped match linked to its dataset import."""

    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_matches_source_external_id"),
        CheckConstraint("home_team_id <> away_team_id", name="different_teams"),
        CheckConstraint(
            "processing_status IN ('pending', 'processing', 'complete', 'failed')",
            name="processing_status_allowed",
        ),
        Index("ix_matches_date_status", "match_date", "processing_status"),
    )

    external_id: Mapped[str] = mapped_column(String(100), nullable=False)
    home_team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False
    )
    away_team_id: Mapped[UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False
    )
    competition: Mapped[str | None] = mapped_column(String(160))
    match_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pitch_length_m: Mapped[float] = mapped_column(Float, nullable=False, default=105.0)
    pitch_width_m: Mapped[float] = mapped_column(Float, nullable=False, default=68.0)
    source: Mapped[str] = mapped_column(String(80), nullable=False)
    dataset_import_id: Mapped[UUID] = mapped_column(
        ForeignKey("dataset_imports.id", ondelete="RESTRICT"), nullable=False
    )
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    processing_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
