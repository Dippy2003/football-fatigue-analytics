"""Tests for deterministic public-demo data."""

import pandas as pd

from app.data.synthetic import generate_synthetic_match


def test_synthetic_match_is_deterministic() -> None:
    first = generate_synthetic_match(seed=42)
    second = generate_synthetic_match(seed=42)

    pd.testing.assert_frame_equal(first.tracking, second.tracking)
    pd.testing.assert_frame_equal(first.events, second.events)


def test_synthetic_match_has_two_teams_periods_and_many_players() -> None:
    match = generate_synthetic_match()

    assert match.tracking["team_id"].nunique() == 2
    assert set(match.tracking["period"]) == {1, 2}
    assert match.tracking["player_id"].nunique() >= 14
    assert match.tracking["is_synthetic"].all()
    assert match.events["is_synthetic"].all()


def test_synthetic_events_cover_supported_families() -> None:
    event_types = set(generate_synthetic_match().events["event_type"])

    assert event_types == {
        "pass",
        "pressure",
        "tackle",
        "interception",
        "possession_loss",
    }


def test_synthetic_tracking_includes_cleanable_dropout() -> None:
    tracking = generate_synthetic_match().tracking

    assert tracking[["x", "y"]].isna().any().all()
