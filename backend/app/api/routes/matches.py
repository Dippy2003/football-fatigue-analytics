"""Stored match discovery and team summary endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Match, Player, PlayerMatchMetric, Team
from app.db.session import get_session
from app.repositories.matches import MatchRepository

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])


class MatchResponse(BaseModel):
    id: UUID
    external_id: str
    competition: str | None
    home_team_id: UUID
    away_team_id: UUID
    is_synthetic: bool
    processing_status: str


def _match_or_404(session: Session, match_id: UUID) -> Match:
    match = MatchRepository(session).get(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return match


@router.get("", response_model=list[MatchResponse])
def list_matches(
    session: Annotated[Session, Depends(get_session)],
) -> list[MatchResponse]:
    """List persisted matches in stable recent-first order."""
    return [
        MatchResponse.model_validate(match, from_attributes=True)
        for match in MatchRepository(session).list()
    ]


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> MatchResponse:
    """Return one persisted match."""
    return MatchResponse.model_validate(
        _match_or_404(session, match_id), from_attributes=True
    )


@router.get("/{match_id}/players")
def match_players(
    match_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> list[dict[str, object]]:
    """Return player identities and supported summary metrics."""
    _match_or_404(session, match_id)
    rows = session.execute(
        select(Player, PlayerMatchMetric)
        .join(PlayerMatchMetric, PlayerMatchMetric.player_id == Player.id)
        .where(PlayerMatchMetric.match_id == match_id)
        .order_by(Player.external_id)
    ).all()
    return [
        {
            "id": player.id,
            "external_id": player.external_id,
            "name": player.name,
            "position": player.position,
            "team_id": player.team_id,
            "total_distance_m": metric.total_distance_m,
            "data_quality_score": metric.data_quality_score,
        }
        for player, metric in rows
    ]


@router.get("/{match_id}/team-summary")
def team_summary(
    match_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> list[dict[str, object]]:
    """Aggregate stored player workload by team."""
    match = _match_or_404(session, match_id)
    summaries: list[dict[str, object]] = []
    for team_id in (match.home_team_id, match.away_team_id):
        team = session.get(Team, team_id)
        metrics = session.scalars(
            select(PlayerMatchMetric)
            .join(Player, Player.id == PlayerMatchMetric.player_id)
            .where(PlayerMatchMetric.match_id == match_id, Player.team_id == team_id)
        ).all()
        summaries.append(
            {
                "team_id": team_id,
                "team_name": team.name if team else "Unknown",
                "player_count": len(metrics),
                "total_distance_m": sum(metric.total_distance_m for metric in metrics),
                "sprint_count": sum(metric.sprint_count for metric in metrics),
            }
        )
    return summaries


@router.get("/{match_id}/quality")
def match_quality(
    match_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> dict[str, object]:
    """Return stored quality evidence independently of risk scores."""
    _match_or_404(session, match_id)
    metrics = session.scalars(
        select(PlayerMatchMetric).where(PlayerMatchMetric.match_id == match_id)
    ).all()
    score = (
        sum(item.data_quality_score for item in metrics) / len(metrics)
        if metrics
        else 0
    )
    return {
        "match_id": match_id,
        "data_quality_score": score,
        "player_metric_coverage": len(metrics),
        "limitations": [] if metrics else ["No player metrics are stored."],
    }
