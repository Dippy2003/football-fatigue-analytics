"""Rights-gated local tracking import and persistence."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.data.importers.metrica import load_metrica_events, load_metrica_tracking
from app.data.processing import ProcessingResult, process_canonical_match
from app.data.registry import SourceRecord
from app.db.models import DatasetImport, Match, Player
from app.repositories.analytics import AnalyticsRepository
from app.repositories.datasets import DatasetRepository
from app.repositories.matches import MatchRepository
from app.repositories.teams import TeamPlayerRepository
from app.services.demo import metric_values


@dataclass(frozen=True)
class ImportResult:
    """Persisted external match identities and quality evidence."""

    dataset_import: DatasetImport
    match: Match
    players: list[Player]
    processing: ProcessingResult
    created: bool


def aggregate_checksum(files: list[tuple[str, bytes]]) -> str:
    """Hash role-delimited bytes so repeated uploads are idempotent."""
    digest = hashlib.sha256()
    for role, content in sorted(files):
        digest.update(role.encode())
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_match(
    tracking: pd.DataFrame,
    events: pd.DataFrame,
    *,
    source_match_id: str,
    max_rows: int,
) -> tuple[str, str]:
    if tracking.empty:
        raise ValueError("Tracking CSV contains no observations.")
    if len(tracking) + len(events) > max_rows:
        raise ValueError("Import exceeds the configured row limit.")
    match_ids = {str(value) for value in tracking["match_id"].dropna().unique()}
    if match_ids != {source_match_id}:
        raise ValueError("Tracking match_id must equal the declared source match ID.")
    if not events.empty:
        event_match_ids = {str(value) for value in events["match_id"].dropna().unique()}
        if event_match_ids != {source_match_id}:
            raise ValueError("Event match_id must equal the declared source match ID.")
    team_ids = sorted(str(value) for value in tracking["team_id"].dropna().unique())
    if len(team_ids) != 2:
        raise ValueError("Tracking data must contain exactly two teams.")
    if tracking["player_id"].isna().any():
        raise ValueError("Every tracking observation must identify a player.")
    return team_ids[0], team_ids[1]


def import_metrica_match(
    session: Session,
    *,
    source: SourceRecord,
    source_match_id: str,
    competition: str,
    tracking_path: Path,
    tracking_bytes: bytes,
    events_path: Path | None,
    events_bytes: bytes | None,
    original_manifest: list[dict[str, object]],
    data_root: Path,
    max_rows: int,
) -> ImportResult:
    """Process authorized local Metrica-compatible files into dashboard data."""
    tracking = load_metrica_tracking(tracking_path)
    events = (
        load_metrica_events(events_path) if events_path is not None else pd.DataFrame()
    )
    home_external_id, away_external_id = _validate_match(
        tracking,
        events,
        source_match_id=source_match_id,
        max_rows=max_rows,
    )
    checksum_inputs = [("tracking", tracking_bytes)]
    if events_bytes is not None:
        checksum_inputs.append(("events", events_bytes))
    checksum = aggregate_checksum(checksum_inputs)
    datasets = DatasetRepository(session)
    existing_import = datasets.get_by_checksum(checksum)
    existing_match = MatchRepository(session).get_by_external_id(
        source=source.id,
        external_id=source_match_id,
    )
    if existing_match is not None and (
        existing_import is None
        or existing_match.dataset_import_id != existing_import.id
    ):
        raise ValueError(
            "This source match ID was already imported with different file content."
        )
    if existing_import is not None and existing_match is not None:
        output_directory = data_root / "processed" / "imports"
        processing = process_canonical_match(
            tracking=tracking,
            events=events,
            output_directory=output_directory,
            output_match_id=str(existing_match.id),
        )
        players = [
            player
            for metric in AnalyticsRepository(session).metrics_for_match(
                existing_match.id
            )
            if (player := session.get(Player, metric.player_id)) is not None
        ]
        return ImportResult(
            dataset_import=existing_import,
            match=existing_match,
            players=players,
            processing=processing,
            created=False,
        )

    dataset_import = datasets.create_if_absent(
        provider=source.provider,
        source_registry_id=source.id,
        checksum=checksum,
        rights_snapshot=source.model_dump(mode="json"),
        manifest=original_manifest,
        is_synthetic=False,
    )
    teams = TeamPlayerRepository(session)
    home = teams.get_or_create_team(
        source=source.id,
        external_id=home_external_id,
        name=home_external_id,
    )
    away = teams.get_or_create_team(
        source=source.id,
        external_id=away_external_id,
        name=away_external_id,
    )
    player_records: list[Player] = []
    player_teams = (
        tracking[["player_id", "team_id"]].drop_duplicates().sort_values("player_id")
    )
    if player_teams["player_id"].duplicated().any():
        raise ValueError("A player cannot belong to both teams in one import.")
    for row in player_teams.itertuples(index=False):
        external_id = str(row.player_id)
        team = home if str(row.team_id) == home_external_id else away
        player_records.append(
            teams.get_or_create_player(
                team=team,
                source=source.id,
                external_id=external_id,
                name=external_id,
                position=None,
            )
        )
    match = MatchRepository(session).create_if_absent(
        source=source.id,
        external_id=source_match_id,
        home_team_id=home.id,
        away_team_id=away.id,
        competition=competition,
        dataset_import_id=dataset_import.id,
        is_synthetic=False,
        processing_status="processing",
    )
    processing = process_canonical_match(
        tracking=tracking,
        events=events,
        output_directory=data_root / "processed" / "imports",
        output_match_id=str(match.id),
    )
    analytics = AnalyticsRepository(session)
    for player in player_records:
        analytics.upsert_metric(
            match_id=match.id,
            player_id=player.id,
            **metric_values(processing, player),
        )
    dataset_import.import_status = "complete"
    match.processing_status = "complete"
    session.commit()
    return ImportResult(
        dataset_import=dataset_import,
        match=match,
        players=player_records,
        processing=processing,
        created=True,
    )
