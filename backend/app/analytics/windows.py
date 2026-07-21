"""Fixed match-window workload summaries."""

from __future__ import annotations

import pandas as pd

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG
from app.analytics.movement import add_speed_features


def summarize_match_windows(
    frame: pd.DataFrame,
    *,
    window_minutes: int = DEFAULT_ANALYTICS_CONFIG.window_minutes,
) -> pd.DataFrame:
    """Aggregate movement into continuous match-time windows."""
    enriched = add_speed_features(frame)
    absolute_seconds = (enriched["period"] - 1) * 45 * 60 + enriched[
        "timestamp_seconds"
    ]
    window_seconds = window_minutes * 60
    enriched["window_start_minute"] = (
        (absolute_seconds // window_seconds) * window_minutes
    ).astype(int)
    return (
        enriched.groupby(["match_id", "player_id", "window_start_minute"], sort=False)
        .agg(
            distance_m=("step_distance_m", "sum"),
            average_speed_mps=("speed_mps", "mean"),
            max_speed_mps=("speed_mps", "max"),
            observed_duration_s=("delta_t_s", "sum"),
        )
        .reset_index()
    )
