"""Speed calculation tests."""

import numpy as np
import pandas as pd

from app.analytics.movement import add_speed_features, summarize_speed


def test_speed_uses_distance_over_positive_time() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 0.5, 1.5],
            "x": [0.0, 2.0, 5.0],
            "y": [0.0, 0.0, 0.0],
        }
    )

    result = add_speed_features(frame)

    speeds = result["speed_mps"].to_numpy(dtype=float)
    assert np.isnan(speeds[0])
    assert speeds[1:].tolist() == [4.0, 3.0]


def test_speed_does_not_cross_period_boundary() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1", "m1"],
            "period": [1, 2],
            "player_id": ["p1", "p1"],
            "timestamp_seconds": [45.0, 0.0],
            "x": [0.0, 100.0],
            "y": [0.0, 60.0],
        }
    )

    assert add_speed_features(frame)["speed_mps"].isna().all()


def test_speed_summary_reports_mean_and_max() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 1.0, 2.0],
            "x": [0.0, 2.0, 6.0],
            "y": [0.0, 0.0, 0.0],
        }
    )

    summary = summarize_speed(frame)

    assert summary.loc[0, "average_speed_mps"] == 3.0
    assert summary.loc[0, "max_speed_mps"] == 4.0
