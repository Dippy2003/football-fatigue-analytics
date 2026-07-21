"""Acceleration and deceleration tests."""

import pandas as pd

from app.analytics.movement import add_acceleration_features


def test_acceleration_and_deceleration_are_separated() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 4,
            "period": [1] * 4,
            "player_id": ["p1"] * 4,
            "timestamp_seconds": [0.0, 1.0, 2.0, 3.0],
            "x": [0.0, 1.0, 4.0, 6.0],
            "y": [0.0] * 4,
        }
    )

    result = add_acceleration_features(frame)

    assert result.loc[2, "acceleration_mps2"] == 2.0
    assert result.loc[2, "positive_acceleration_mps2"] == 2.0
    assert result.loc[2, "deceleration_mps2"] == 0.0
    assert result.loc[3, "acceleration_mps2"] == -1.0
    assert result.loc[3, "deceleration_mps2"] == 1.0
