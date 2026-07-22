"""Player-match analytical feature persistence."""

from uuid import UUID

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PlayerMatchMetric(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Queryable summary features for one player in one match."""

    __tablename__ = "player_match_metrics"
    __table_args__ = (
        UniqueConstraint("match_id", "player_id", name="uq_metrics_match_player"),
        Index("ix_metrics_player_created", "player_id", "created_at"),
    )

    match_id: Mapped[UUID] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"), nullable=False
    )
    player_id: Mapped[UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    playing_minutes: Mapped[float] = mapped_column(Float, nullable=False)
    total_distance_m: Mapped[float] = mapped_column(Float, nullable=False)
    distance_per_minute: Mapped[float] = mapped_column(Float, nullable=False)
    average_speed_mps: Mapped[float] = mapped_column(Float, nullable=False)
    max_speed_mps: Mapped[float] = mapped_column(Float, nullable=False)
    high_speed_distance_m: Mapped[float] = mapped_column(Float, nullable=False)
    sprint_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sprint_distance_m: Mapped[float] = mapped_column(Float, nullable=False)
    median_sprint_recovery_seconds: Mapped[float | None] = mapped_column(Float)
    acceleration_count: Mapped[int] = mapped_column(Integer, nullable=False)
    deceleration_count: Mapped[int] = mapped_column(Integer, nullable=False)
    second_half_speed_change_pct: Mapped[float | None] = mapped_column(Float)
    late_match_sprint_change_pct: Mapped[float | None] = mapped_column(Float)
    late_match_distance_change_pct: Mapped[float | None] = mapped_column(Float)
    pass_accuracy_change_pct: Mapped[float | None] = mapped_column(Float)
    pressure_change_pct: Mapped[float | None] = mapped_column(Float)
    possession_loss_change: Mapped[float | None] = mapped_column(Float)
    workload_vs_baseline_zscore: Mapped[float | None] = mapped_column(Float)
    data_quality_score: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_type: Mapped[str | None] = mapped_column(String(50))
    baseline_confidence: Mapped[float | None] = mapped_column(Float)
    supported_event_metrics: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    feature_version: Mapped[str] = mapped_column(String(40), nullable=False)
