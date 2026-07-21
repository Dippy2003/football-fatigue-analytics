"""Distance feature tests."""

import pandas as pd
import pytest

from app.analytics.movement import add_distance_features, summarize_distance


def sample_track() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 1.0, 2.0],
            "x": [0.0, 3.0, 6.0],
            "y": [0.0, 4.0, 8.0],
        }
    )


def test_step_and_total_distance_use_euclidean_metres() -> None:
    result = add_distance_features(sample_track())

    assert result["step_distance_m"].tolist() == [0.0, 5.0, 5.0]
    assert result["total_distance_m"].tolist() == [0.0, 5.0, 10.0]


def test_missing_coordinate_does_not_create_distance_jump() -> None:
    frame = sample_track()
    frame.loc[1, ["x", "y"]] = None

    assert add_distance_features(frame)["step_distance_m"].sum() == 0


def test_distance_summary_uses_active_duration() -> None:
    summary = summarize_distance(sample_track())

    assert summary.loc[0, "total_distance_m"] == 10
    assert summary.loc[0, "distance_per_active_min_m"] == pytest.approx(300)
