"""Tracking cleaning tests."""

import pandas as pd

from app.data.cleaning import (
    interpolate_short_tracking_gaps,
    sort_and_deduplicate_tracking,
)


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


def test_short_gap_is_interpolated_and_flagged() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 0.1, 0.2],
            "x": [0.0, None, 2.0],
            "y": [0.0, None, 4.0],
        }
    )

    result = interpolate_short_tracking_gaps(frame)

    assert (result.frame.loc[1, "x"], result.frame.loc[1, "y"]) == (1.0, 2.0)
    assert bool(result.frame.loc[1, "was_interpolated"])
    assert result.flags[0].code == "short_tracking_gaps_interpolated"


def test_interpolation_never_crosses_period_or_long_gap() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 4,
            "period": [1, 1, 1, 2],
            "player_id": ["p1"] * 4,
            "timestamp_seconds": [0.0, 0.4, 1.0, 0.0],
            "x": [0.0, None, 10.0, None],
            "y": [0.0, None, 10.0, None],
        }
    )

    result = interpolate_short_tracking_gaps(frame)

    assert result.frame[["x", "y"]].isna().iloc[[1, 3]].all().all()
    assert result.flags[-1].code == "tracking_gaps_unresolved"
