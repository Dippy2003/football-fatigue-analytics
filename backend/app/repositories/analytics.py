"""Metric and risk-assessment repository operations."""

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import PlayerMatchMetric, RiskAssessment


class AnalyticsRepository:
    """Persist and query derived player-match analytics."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_metric(self, **values: Any) -> PlayerMatchMetric:
        metric = self.session.scalar(
            select(PlayerMatchMetric).where(
                PlayerMatchMetric.match_id == values["match_id"],
                PlayerMatchMetric.player_id == values["player_id"],
            )
        )
        if metric is None:
            metric = PlayerMatchMetric(**values)
            self.session.add(metric)
        else:
            for name, value in values.items():
                setattr(metric, name, value)
        self.session.flush()
        return metric

    def metrics_for_match(self, match_id: UUID) -> list[PlayerMatchMetric]:
        return list(
            self.session.scalars(
                select(PlayerMatchMetric)
                .where(PlayerMatchMetric.match_id == match_id)
                .order_by(PlayerMatchMetric.player_id)
            )
        )

    def save_risk(self, **values: Any) -> RiskAssessment:
        assessment = RiskAssessment(**values)
        self.session.add(assessment)
        self.session.flush()
        return assessment

    def latest_risk(self, *, match_id: UUID, player_id: UUID) -> RiskAssessment | None:
        return self.session.scalar(
            select(RiskAssessment)
            .where(
                RiskAssessment.match_id == match_id,
                RiskAssessment.player_id == player_id,
            )
            .order_by(RiskAssessment.created_at.desc())
            .limit(1)
        )
