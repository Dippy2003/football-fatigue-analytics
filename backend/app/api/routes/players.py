"""Player profiles, metrics, timelines, heatmaps, and event endpoints."""

from typing import Annotated, cast
from uuid import UUID

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.data.storage import read_match_parquet
from app.data.synthetic import generate_synthetic_match
from app.db.models import Match, Player, PlayerMatchMetric
from app.db.session import get_session

router = APIRouter(prefix="/api/v1", tags=["players"])


def _player(session: Session, player_id: UUID) -> Player:
    player = session.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found.")
    return player


def _metric(session: Session, match_id: UUID, player_id: UUID) -> PlayerMatchMetric:
    metric = session.scalar(
        select(PlayerMatchMetric).where(
            PlayerMatchMetric.match_id == match_id,
            PlayerMatchMetric.player_id == player_id,
        )
    )
    if metric is None:
        raise HTTPException(status_code=404, detail="Player metrics not found.")
    return metric


def _settings(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


@router.get("/players/{player_id}")
def player_profile(
    player_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> dict[str, object]:
    player = _player(session, player_id)
    return {
        "id": player.id,
        "external_id": player.external_id,
        "name": player.name,
        "position": player.position,
        "team_id": player.team_id,
        "source": player.source,
    }


@router.get("/players/{player_id}/matches")
def player_matches(
    player_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> list[dict[str, object]]:
    _player(session, player_id)
    rows = session.execute(
        select(Match, PlayerMatchMetric)
        .join(PlayerMatchMetric, PlayerMatchMetric.match_id == Match.id)
        .where(PlayerMatchMetric.player_id == player_id)
        .order_by(Match.match_date.desc())
    ).all()
    return [
        {
            "match_id": match.id,
            "external_id": match.external_id,
            "competition": match.competition,
            "playing_minutes": metric.playing_minutes,
            "total_distance_m": metric.total_distance_m,
        }
        for match, metric in rows
    ]


@router.get("/matches/{match_id}/players/{player_id}/metrics")
def player_metrics(
    match_id: UUID, player_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> dict[str, object]:
    metric = _metric(session, match_id, player_id)
    return {
        column.name: getattr(metric, column.name)
        for column in PlayerMatchMetric.__table__.columns
        if column.name not in {"created_at", "updated_at"}
    }


def _match(session: Session, match_id: UUID) -> Match:
    match = session.get(Match, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return match


def _processed_table(request: Request, match: Match, table: str) -> pd.DataFrame:
    path = (
        _settings(request).data_root
        / "processed"
        / "imports"
        / f"{match.id}.{table}.parquet"
    )
    if not path.is_file():
        raise HTTPException(
            status_code=409,
            detail="Processed local match data is unavailable; import it again.",
        )
    return read_match_parquet(path)


def _tracking_for_player(
    request: Request, match: Match, player: Player
) -> pd.DataFrame:
    tracking = (
        generate_synthetic_match(seed=_settings(request).synthetic_seed).tracking
        if match.is_synthetic
        else _processed_table(request, match, "tracking")
    )
    return tracking[tracking["player_id"].astype(str) == player.external_id]


@router.get("/matches/{match_id}/players/{player_id}/timeline")
def player_timeline(
    match_id: UUID,
    player_id: UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    _metric(session, match_id, player_id)
    player = _player(session, player_id)
    tracking = _tracking_for_player(request, _match(session, match_id), player)
    step = max(1, len(tracking) // 120)
    sampled = tracking.dropna(subset=["period", "timestamp_seconds", "x", "y"]).iloc[
        ::step
    ]
    return {
        "downsampled": step > 1,
        "point_count": len(sampled),
        "points": sampled[["period", "timestamp_seconds", "x", "y"]].to_dict("records"),
    }


@router.get("/matches/{match_id}/players/{player_id}/heatmap")
def player_heatmap(
    match_id: UUID,
    player_id: UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    _metric(session, match_id, player_id)
    player = _player(session, player_id)
    tracking = _tracking_for_player(request, _match(session, match_id), player)
    observed = tracking[["x", "y"]].dropna()
    grid, _, _ = np.histogram2d(
        observed["y"],
        observed["x"],
        bins=(8, 12),
        range=((0, 68), (0, 105)),
    )
    return {
        "rows": 8,
        "columns": 12,
        "max_count": int(grid.max()),
        "grid": grid.astype(int).tolist(),
    }


@router.get("/matches/{match_id}/players/{player_id}/events")
def player_events(
    match_id: UUID,
    player_id: UUID,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    _metric(session, match_id, player_id)
    player = _player(session, player_id)
    match = _match(session, match_id)
    events = (
        generate_synthetic_match(seed=_settings(request).synthetic_seed).events
        if match.is_synthetic
        else _processed_table(request, match, "events")
    )
    supported = events[events["player_id"].astype(str) == player.external_id]
    serializable = supported.astype(object)
    serializable[serializable.isna()] = None
    return {
        "supported": not events.empty,
        "events": serializable.to_dict("records"),
    }


@router.get("/players/{player_id}/baseline")
def player_baseline(
    player_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> dict[str, object]:
    _player(session, player_id)
    metric = session.scalar(
        select(PlayerMatchMetric)
        .where(PlayerMatchMetric.player_id == player_id)
        .order_by(PlayerMatchMetric.created_at.desc())
    )
    if metric is None:
        raise HTTPException(status_code=404, detail="Baseline not found.")
    return {
        "baseline_type": metric.baseline_type,
        "baseline_confidence": metric.baseline_confidence,
        "workload_zscore": metric.workload_vs_baseline_zscore,
        "sample_size": 1,
        "limitation": "Match-only comparison until historical matches exist.",
    }
