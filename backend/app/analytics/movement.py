"""Provider-neutral movement feature calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd

PLAYER_PERIOD = ["match_id", "period", "player_id"]


def add_distance_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate valid step distance and cumulative player distance in metres."""
    result = frame.sort_values(
        [*PLAYER_PERIOD, "timestamp_seconds"], kind="stable"
    ).copy()
    grouped = result.groupby(PLAYER_PERIOD, sort=False)
    dx = grouped["x"].diff()
    dy = grouped["y"].diff()
    step_distance = pd.Series(np.hypot(dx, dy), index=result.index)
    result["step_distance_m"] = step_distance.fillna(0.0)
    invalid_step = result[["x", "y"]].isna().any(axis=1) | grouped[
        ["x", "y"]
    ].shift().isna().any(axis=1)
    result.loc[invalid_step, "step_distance_m"] = 0.0
    result["total_distance_m"] = result.groupby(PLAYER_PERIOD, sort=False)[
        "step_distance_m"
    ].cumsum()
    return result


def summarize_distance(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize total distance, active time, and distance per active minute."""
    enriched = add_distance_features(frame)
    grouped = enriched.groupby(["match_id", "player_id"], sort=False)
    summary = grouped.agg(
        total_distance_m=("step_distance_m", "sum"),
        active_duration_s=(
            "timestamp_seconds",
            lambda values: values.max() - values.min(),
        ),
    ).reset_index()
    active_minutes = summary["active_duration_s"] / 60
    summary["distance_per_active_min_m"] = summary["total_distance_m"].div(
        active_minutes.where(active_minutes > 0)
    )
    return summary


def add_speed_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate instantaneous speed using only positive in-period time deltas."""
    result = add_distance_features(frame)
    delta_t = result.groupby(PLAYER_PERIOD, sort=False)["timestamp_seconds"].diff()
    valid_delta = delta_t > 0
    result["delta_t_s"] = delta_t.where(valid_delta)
    result["speed_mps"] = result["step_distance_m"].div(result["delta_t_s"])
    return result


def summarize_speed(frame: pd.DataFrame) -> pd.DataFrame:
    """Return average and maximum observed speeds per player."""
    enriched = add_speed_features(frame)
    return (
        enriched.groupby(["match_id", "player_id"], sort=False)
        .agg(
            average_speed_mps=("speed_mps", "mean"), max_speed_mps=("speed_mps", "max")
        )
        .reset_index()
    )
