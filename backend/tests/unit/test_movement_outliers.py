"""Physiological outlier tests."""

import pandas as pd

from app.analytics.movement import flag_physiological_outliers


def test_unrealistic_jump_is_flagged_not_removed() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1", "m1"],
            "period": [1, 1],
            "player_id": ["p1", "p1"],
            "timestamp_seconds": [0.0, 0.1],
            "x": [0.0, 20.0],
            "y": [0.0, 0.0],
        }
    )

    result = flag_physiological_outliers(frame)

    assert len(result) == 2
    assert bool(result.loc[1, "is_speed_outlier"])
    assert bool(result.loc[1, "quality_excluded"])


def test_boundary_speed_is_not_flagged() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1", "m1"],
            "period": [1, 1],
            "player_id": ["p1", "p1"],
            "timestamp_seconds": [0.0, 1.0],
            "x": [0.0, 12.5],
            "y": [0.0, 0.0],
        }
    )

    assert not flag_physiological_outliers(frame)["is_speed_outlier"].any()
