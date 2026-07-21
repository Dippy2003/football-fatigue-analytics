"""Speed intensity zones and workload summaries."""

from __future__ import annotations

import pandas as pd

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG
from app.analytics.movement import add_speed_features

ZONE_LABELS = ("recovery", "low", "moderate", "high", "sprint")


def classify_intensity_zones(frame: pd.DataFrame) -> pd.DataFrame:
    """Assign documented speed bands to each valid observation."""
    result = add_speed_features(frame)
    edges = DEFAULT_ANALYTICS_CONFIG.intensity_zone_edges_mps
    result["intensity_zone"] = pd.cut(
        result["speed_mps"].round(6),
        bins=[float("-inf"), *edges, float("inf")],
        labels=ZONE_LABELS,
        right=False,
    )
    return result


def summarize_intensity_zones(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate time and distance by player and intensity band."""
    enriched = classify_intensity_zones(frame)
    valid = enriched.dropna(subset=["intensity_zone", "delta_t_s"])
    return (
        valid.groupby(
            ["match_id", "player_id", "intensity_zone"],
            observed=True,
            sort=False,
        )
        .agg(duration_s=("delta_t_s", "sum"), distance_m=("step_distance_m", "sum"))
        .reset_index()
    )
