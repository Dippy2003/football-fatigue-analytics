"""Rights-gated adapter for developer-supplied StatsBomb event JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from app.data.coordinates import convert_xy, validate_pitch_bounds
from app.data.importers.common import require_local_file


def _location(value: object) -> tuple[float | None, float | None]:
    if not isinstance(value, list) or len(value) < 2:
        return None, None
    return float(value[0]), float(value[1])


def load_statsbomb_events(
    path: Path, *, match_id: str, rights_acknowledged: bool = False
) -> pd.DataFrame:
    """Load local event JSON only after an explicit current-rights check."""
    if not rights_acknowledged:
        raise PermissionError(
            "StatsBomb import is disabled until current terms are acknowledged"
        )
    with require_local_file(path).open(encoding="utf-8") as event_file:
        payload: Any = json.load(event_file)
    if not isinstance(payload, list):
        raise ValueError("StatsBomb event JSON must contain a list")
    rows: list[dict[str, object]] = []
    for event in payload:
        if not isinstance(event, dict):
            raise ValueError("StatsBomb event entries must be objects")
        start_x, start_y = _location(event.get("location"))
        event_type = event.get("type", {})
        player = event.get("player", {})
        team = event.get("team", {})
        detail = event.get(str(event_type.get("name", "")).lower(), {})
        end_x, end_y = _location(detail.get("end_location"))
        rows.append(
            {
                "match_id": match_id,
                "event_id": str(event.get("id", "")),
                "period": int(event.get("period", 0)),
                "timestamp_seconds": float(event.get("minute", 0)) * 60
                + float(event.get("second", 0)),
                "team_id": str(team.get("id", "")),
                "player_id": str(player.get("id")) if player else None,
                "event_type": str(event_type.get("name", "unknown")).lower(),
                "outcome": detail.get("outcome", {}).get("name"),
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y,
                "source": "statsbomb_open_data",
                "is_synthetic": False,
            }
        )
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame = convert_xy(
        frame, x_column="start_x", y_column="start_y", system="statsbomb"
    )
    frame = convert_xy(frame, x_column="end_x", y_column="end_y", system="statsbomb")
    validate_pitch_bounds(
        frame, coordinate_pairs=(("start_x", "start_y"), ("end_x", "end_y"))
    )
    return frame
