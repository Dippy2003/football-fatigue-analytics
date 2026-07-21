"""Tracking cleaning tests."""

import pandas as pd

from app.data.cleaning import sort_and_deduplicate_tracking


def test_sort_and_deduplicate_keeps_first_observation() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1", "m1", "m1"],
            "period": [1, 1, 1],
            "player_id": ["p1", "p1", "p1"],
            "timestamp_seconds": [2.0, 1.0, 1.0],
            "x": [2.0, 1.0, 99.0],
            "y": [2.0, 1.0, 99.0],
        }
    )

    result = sort_and_deduplicate_tracking(frame)

    assert result.frame["timestamp_seconds"].tolist() == [1.0, 2.0]
    assert result.frame["x"].tolist() == [1.0, 2.0]
    assert result.flags[0].row_count == 1


def test_clean_unique_rows_have_no_flags() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"],
            "period": [1],
            "player_id": ["p1"],
            "timestamp_seconds": [0.0],
        }
    )

    assert sort_and_deduplicate_tracking(frame).flags == ()
