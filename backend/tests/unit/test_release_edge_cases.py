"""Cross-module analytical edge cases remain finite and explicit."""

import numpy as np
import pandas as pd

from app.analytics.movement import add_speed_features
from app.analytics.windows import summarize_match_windows


def test_zero_time_delta_never_produces_infinite_speed() -> None:
    frame = pd.DataFrame(
        [
            {
                "match_id": "m",
                "period": 1,
                "player_id": "p",
                "timestamp_seconds": 0.0,
                "x": 0.0,
                "y": 0.0,
            },
            {
                "match_id": "m",
                "period": 1,
                "player_id": "p",
                "timestamp_seconds": 0.0,
                "x": 1.0,
                "y": 1.0,
            },
        ]
    )

    result = add_speed_features(frame)

    assert not np.isinf(result["speed_mps"]).any()


def test_window_assignment_respects_second_period_offset() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m", "m"],
            "period": [1, 2],
            "player_id": ["p", "p"],
            "timestamp_seconds": [899.9, 0.0],
            "x": [0.0, 0.0],
            "y": [0.0, 0.0],
        }
    )

    result = summarize_match_windows(frame)

    assert list(result["window_start_minute"]) == [0, 45]
