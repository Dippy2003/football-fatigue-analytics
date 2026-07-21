"""Local-only Metrica-compatible tabular adapters.

No sample data is downloaded or bundled. Developers must provide files whose
rights they have independently checked.
"""

from pathlib import Path

import pandas as pd

from app.data.coordinates import convert_xy, validate_pitch_bounds
from app.data.importers.common import require_columns, require_local_file

TRACKING_COLUMNS = {
    "match_id",
    "period",
    "frame_id",
    "timestamp_seconds",
    "team_id",
    "player_id",
    "x",
    "y",
    "ball_x",
    "ball_y",
}
EVENT_COLUMNS = {
    "match_id",
    "event_id",
    "period",
    "timestamp_seconds",
    "team_id",
    "event_type",
    "start_x",
    "start_y",
}


def load_metrica_tracking(path: Path) -> pd.DataFrame:
    """Load a developer-supplied long-form normalized tracking CSV."""
    frame = pd.read_csv(require_local_file(path))
    require_columns(frame, TRACKING_COLUMNS)
    canonical = convert_xy(frame, x_column="x", y_column="y", system="normalized")
    canonical = convert_xy(
        canonical, x_column="ball_x", y_column="ball_y", system="normalized"
    )
    validate_pitch_bounds(
        canonical, coordinate_pairs=(("x", "y"), ("ball_x", "ball_y"))
    )
    canonical["source"] = "metrica_sample_data"
    canonical["is_synthetic"] = False
    return canonical[
        [
            "match_id",
            "period",
            "frame_id",
            "timestamp_seconds",
            "team_id",
            "player_id",
            "x",
            "y",
            "ball_x",
            "ball_y",
            "source",
            "is_synthetic",
        ]
    ]


def load_metrica_events(path: Path) -> pd.DataFrame:
    """Load developer-supplied long-form normalized Metrica events."""
    frame = pd.read_csv(require_local_file(path))
    require_columns(frame, EVENT_COLUMNS)
    canonical = convert_xy(
        frame, x_column="start_x", y_column="start_y", system="normalized"
    )
    if {"end_x", "end_y"}.issubset(canonical.columns):
        canonical = convert_xy(
            canonical, x_column="end_x", y_column="end_y", system="normalized"
        )
    else:
        canonical[["end_x", "end_y"]] = pd.NA
    validate_pitch_bounds(
        canonical, coordinate_pairs=(("start_x", "start_y"), ("end_x", "end_y"))
    )
    canonical["player_id"] = canonical.get("player_id", pd.Series(dtype="object"))
    canonical["outcome"] = canonical.get("outcome", pd.Series(dtype="object"))
    canonical["source"] = "metrica_sample_data"
    canonical["is_synthetic"] = False
    return canonical[
        [
            "match_id",
            "event_id",
            "period",
            "timestamp_seconds",
            "team_id",
            "player_id",
            "event_type",
            "outcome",
            "start_x",
            "start_y",
            "end_x",
            "end_y",
            "source",
            "is_synthetic",
        ]
    ]
