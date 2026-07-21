"""Sprint bout detection tests."""

import pandas as pd
import pytest

from app.analytics.sprints import detect_sprints


def make_track(speeds: list[float], interval: float = 0.1) -> pd.DataFrame:
    x = [0.0]
    for speed in speeds:
        x.append(x[-1] + speed * interval)
    return pd.DataFrame(
        {
            "match_id": ["m1"] * len(x),
            "period": [1] * len(x),
            "player_id": ["p1"] * len(x),
            "timestamp_seconds": [index * interval for index in range(len(x))],
            "x": x,
            "y": [0.0] * len(x),
        }
    )


def test_sprint_requires_minimum_duration() -> None:
    assert detect_sprints(make_track([8.0] * 4)).empty
    assert len(detect_sprints(make_track([8.0] * 5))) == 1


def test_sprint_summary_reports_distance_and_peak() -> None:
    sprint = detect_sprints(make_track([7.0, 8.0, 9.0, 8.0, 7.0])).iloc[0]

    assert sprint["duration_s"] == 0.5
    assert sprint["distance_m"] == pytest.approx(3.9)
    assert sprint["peak_speed_mps"] == pytest.approx(9.0)


def test_subthreshold_movement_is_not_a_sprint() -> None:
    assert detect_sprints(make_track([6.9] * 10)).empty
