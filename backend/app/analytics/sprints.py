"""Threshold-based, explainable sprint detection."""

from __future__ import annotations

import pandas as pd

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG
from app.analytics.movement import PLAYER_PERIOD, add_speed_features


def detect_sprints(
    frame: pd.DataFrame,
    *,
    threshold_mps: float = 7.0,
    min_duration_s: float = DEFAULT_ANALYTICS_CONFIG.sprint_min_duration_s,
    merge_gap_s: float = DEFAULT_ANALYTICS_CONFIG.sprint_merge_gap_s,
) -> pd.DataFrame:
    """Return sprint bouts with duration, distance, and peak speed."""
    enriched = add_speed_features(frame)
    active = enriched[enriched["speed_mps"] >= threshold_mps].copy()
    bouts: list[dict[str, object]] = []
    for keys, group in active.groupby(PLAYER_PERIOD, sort=False):
        group = group.sort_values("timestamp_seconds")
        boundaries = group["timestamp_seconds"].diff().fillna(0) > (
            group["delta_t_s"].fillna(0) + merge_gap_s
        )
        for _, bout in group.groupby(boundaries.cumsum(), sort=False):
            duration = float(bout["delta_t_s"].sum())
            if duration < min_duration_s:
                continue
            match_id, period, player_id = keys
            bouts.append(
                {
                    "match_id": match_id,
                    "period": period,
                    "player_id": player_id,
                    "start_seconds": float(
                        bout["timestamp_seconds"].iloc[0] - bout["delta_t_s"].iloc[0]
                    ),
                    "end_seconds": float(bout["timestamp_seconds"].iloc[-1]),
                    "duration_s": duration,
                    "distance_m": float(bout["step_distance_m"].sum()),
                    "peak_speed_mps": float(bout["speed_mps"].max()),
                }
            )
    return pd.DataFrame(bouts)
