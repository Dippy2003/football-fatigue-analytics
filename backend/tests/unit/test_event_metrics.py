"""Supported event metric tests."""

import pandas as pd

from app.analytics.events import summarize_event_metrics


def test_event_metrics_count_supported_actions() -> None:
    events = pd.DataFrame(
        {
            "match_id": ["m1"] * 6,
            "team_id": ["home"] * 6,
            "player_id": ["p1"] * 6,
            "event_id": [f"e{i}" for i in range(6)],
            "event_type": [
                "pass",
                "pass",
                "pressure",
                "tackle",
                "interception",
                "possession_loss",
            ],
            "outcome": ["complete", "incomplete", None, None, None, None],
        }
    )

    row = summarize_event_metrics(events).iloc[0]

    assert row["event_count"] == 6
    assert row["pass_attempts"] == 2
    assert row["completed_passes"] == 1
    assert row["pass_completion_rate"] == 0.5
    assert row["defensive_actions"] == 3
    assert row["possession_losses"] == 1


def test_no_passes_produces_unknown_completion_rate() -> None:
    events = pd.DataFrame(
        {
            "match_id": ["m1"],
            "team_id": ["home"],
            "player_id": ["p1"],
            "event_id": ["e1"],
            "event_type": ["tackle"],
            "outcome": [None],
        }
    )

    assert pd.isna(summarize_event_metrics(events).loc[0, "pass_completion_rate"])
