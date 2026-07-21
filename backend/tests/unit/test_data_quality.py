"""Data-quality score tests."""

import pandas as pd

from app.data.quality import build_quality_report


def test_empty_tracking_has_unavailable_quality() -> None:
    report = build_quality_report(pd.DataFrame())

    assert report.quality_score == 0
    assert report.confidence == "unavailable"


def test_complete_plausible_tracking_has_high_quality() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 1.0, 2.0],
            "x": [0.0, 1.0, 2.0],
            "y": [0.0, 0.0, 0.0],
        }
    )

    report = build_quality_report(frame)

    assert report.quality_score == 100
    assert report.confidence == "high"
    assert report.limitations == []


def test_missing_and_implausible_rows_lower_score_with_explanation() -> None:
    frame = pd.DataFrame(
        {
            "match_id": ["m1"] * 3,
            "period": [1] * 3,
            "player_id": ["p1"] * 3,
            "timestamp_seconds": [0.0, 0.1, 0.2],
            "x": [0.0, 50.0, None],
            "y": [0.0, 0.0, None],
        }
    )

    report = build_quality_report(frame)

    assert report.quality_score < 90
    assert len(report.limitations) == 2
