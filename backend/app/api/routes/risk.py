"""Explainable risk-indicator and player-comparison endpoints."""

from dataclasses import asdict
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.risk import RiskInputs, calculate_risk
from app.db.models import Player, PlayerMatchMetric
from app.db.session import get_session
from app.repositories.analytics import AnalyticsRepository

router = APIRouter(prefix="/api/v1", tags=["risk-and-comparison"])


def _risk_inputs(metric: PlayerMatchMetric) -> RiskInputs:
    return RiskInputs(
        speed_decline_pct=(
            max(0.0, -metric.second_half_speed_change_pct)
            if metric.second_half_speed_change_pct is not None
            else None
        ),
        sprint_frequency_decline_pct=(
            max(0.0, -metric.late_match_sprint_change_pct)
            if metric.late_match_sprint_change_pct is not None
            else None
        ),
        workload_vs_baseline_zscore=metric.workload_vs_baseline_zscore,
        event_performance_decline_pct=(
            max(0.0, -metric.pass_accuracy_change_pct)
            if metric.pass_accuracy_change_pct is not None
            else None
        ),
        data_quality=metric.data_quality_score,
        baseline_confidence=metric.baseline_confidence or 0,
    )


@router.get("/matches/{match_id}/players/{player_id}/risk")
def player_risk(
    match_id: UUID,
    player_id: UUID,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    """Calculate and store a deterministic performance-risk indicator."""
    metric = session.scalar(
        select(PlayerMatchMetric).where(
            PlayerMatchMetric.match_id == match_id,
            PlayerMatchMetric.player_id == player_id,
        )
    )
    if metric is None:
        raise HTTPException(status_code=404, detail="Player metrics not found.")
    result = calculate_risk(
        _risk_inputs(metric), baseline_type=metric.baseline_type or "insufficient"
    )
    payload = asdict(result)
    payload["calculated_at"] = result.calculated_at.isoformat()
    repository = AnalyticsRepository(session)
    repository.save_risk(
        match_id=match_id,
        player_id=player_id,
        assessment_status=result.assessment_status,
        score=result.score,
        category=result.category,
        confidence=result.confidence,
        rule_score=result.score,
        anomaly_score=None,
        explanation_json=payload,
        model_version=result.model_version,
    )
    session.commit()
    return payload


@router.get("/matches/{match_id}/compare-players")
def compare_players(
    match_id: UUID,
    player_ids: Annotated[list[UUID], Query(min_length=2, max_length=4)],
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    """Return aligned stored features for two to four players."""
    rows = session.execute(
        select(Player, PlayerMatchMetric)
        .join(PlayerMatchMetric, PlayerMatchMetric.player_id == Player.id)
        .where(
            PlayerMatchMetric.match_id == match_id,
            PlayerMatchMetric.player_id.in_(player_ids),
        )
    ).all()
    if len(rows) != len(set(player_ids)):
        raise HTTPException(
            status_code=404, detail="One or more players were not found."
        )
    return {
        "match_id": match_id,
        "players": [
            {
                "player_id": player.id,
                "name": player.name,
                "position": player.position,
                "total_distance_m": metric.total_distance_m,
                "max_speed_mps": metric.max_speed_mps,
                "sprint_count": metric.sprint_count,
                "data_quality_score": metric.data_quality_score,
            }
            for player, metric in rows
        ],
        "warning": (
            "Goalkeeper and outfield roles should not be compared without context."
        ),
    }
