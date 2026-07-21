"""Speed smoothing tests."""

import pandas as pd
import pytest

from app.analytics.movement import add_smoothed_speed


def test_centered_median_reduces_single_sample_spike() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 5,
            "period": [1] * 5,
            "player_id": ["p1"] * 5,
            "timestamp_seconds": [0.0, 0.1, 0.2, 0.3, 0.4],
            "x": [0.0, 0.1, 5.1, 5.2, 5.3],
            "y": [0.0] * 5,
        }
    )

    result = add_smoothed_speed(frame, window_s=0.3)

    speeds = result["speed_mps"].to_numpy(dtype=float)
    smoothed = result["smoothed_speed_mps"].to_numpy(dtype=float)
    assert speeds[2] > 40
    assert smoothed[2] == pytest.approx(1.0)


def test_smoothing_stays_within_player_period() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 4,
            "period": [1, 1, 2, 2],
            "player_id": ["p1"] * 4,
            "timestamp_seconds": [0.0, 0.1, 0.0, 0.1],
            "x": [0.0, 0.1, 0.0, 1.0],
            "y": [0.0] * 4,
        }
    )

    result = add_smoothed_speed(frame, window_s=0.3)

    assert result.loc[1, "smoothed_speed_mps"] == 1.0
    assert result.loc[3, "smoothed_speed_mps"] == 10.0
