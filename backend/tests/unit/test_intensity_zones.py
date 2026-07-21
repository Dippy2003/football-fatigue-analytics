"""Intensity-zone boundary and summary tests."""

import pandas as pd

from app.analytics.intensity import classify_intensity_zones, summarize_intensity_zones


def speed_track() -> pd.DataFrame:
    speeds = [0.0, 1.9, 2.0, 4.0, 5.5, 7.0]
    positions = [0.0]
    for speed in speeds[1:]:
        positions.append(positions[-1] + speed)
    return pd.DataFrame(
        {
            "match_id": ["m1"] * 6,
            "period": [1] * 6,
            "player_id": ["p1"] * 6,
            "timestamp_seconds": list(map(float, range(6))),
            "x": positions,
            "y": [0.0] * 6,
        }
    )


def test_zone_edges_are_lower_bound_inclusive() -> None:
    zones = classify_intensity_zones(speed_track())["intensity_zone"].astype("string")

    assert zones.iloc[1:].tolist() == [
        "recovery",
        "low",
        "moderate",
        "high",
        "sprint",
    ]


def test_zone_summary_accounts_for_valid_steps() -> None:
    summary = summarize_intensity_zones(speed_track())

    assert summary["duration_s"].sum() == 5
    assert summary["distance_m"].sum() == sum([1.9, 2.0, 4.0, 5.5, 7.0])
