"""Fixed match-window tests."""

import pandas as pd

from app.analytics.windows import summarize_match_windows


def test_fifteen_minute_windows_use_continuous_match_time() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 4,
            "period": [1, 1, 1, 2],
            "player_id": ["p1"] * 4,
            "timestamp_seconds": [0.0, 899.0, 900.0, 0.0],
            "x": [0.0, 1.0, 2.0, 2.0],
            "y": [0.0] * 4,
        }
    )

    result = summarize_match_windows(frame)

    assert result["window_start_minute"].tolist() == [0, 15, 45]


def test_window_summary_reports_observed_duration_and_distance() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 10.0, 20.0],
            "x": [0.0, 2.0, 5.0],
            "y": [0.0] * 3,
        }
    )

    row = summarize_match_windows(frame).iloc[0]

    assert row["observed_duration_s"] == 20
    assert row["distance_m"] == 5
