"""Explainable performance-risk assessment persistence."""

from uuid import UUID

from sqlalchemy import JSON, CheckConstraint, Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RiskAssessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Versioned non-medical indicator result and its full explanation."""

    __tablename__ = "risk_assessments"
    __table_args__ = (
        CheckConstraint(
            "assessment_status IN ('available', 'insufficient_data')",
            name="assessment_status_allowed",
        ),
        CheckConstraint(
            "score IS NULL OR (score >= 0 AND score <= 100)", name="score_bounds"
        ),
        Index("ix_risk_match_player_created", "match_id", "player_id", "created_at"),
    )

    match_id: Mapped[UUID] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"), nullable=False
    )
    player_id: Mapped[UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    assessment_status: Mapped[str] = mapped_column(String(30), nullable=False)
    score: Mapped[float | None] = mapped_column(Float)
    category: Mapped[str | None] = mapped_column(String(60))
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    rule_score: Mapped[float | None] = mapped_column(Float)
    anomaly_score: Mapped[float | None] = mapped_column(Float)
    explanation_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    model_version: Mapped[str] = mapped_column(String(60), nullable=False)
