"""Tests for deterministic public-demo data."""

import pandas as pd
import pytest

from app.analytics.sprints import detect_sprints
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
    one_player_period = tracking[
        (tracking["player_id"] == "home-01") & (tracking["period"] == 1)
    ]
    assert one_player_period["timestamp_seconds"].diff().min() == pytest.approx(0.1)


def test_synthetic_match_includes_second_period_substitutions() -> None:
    tracking = generate_synthetic_match().tracking
    substitute = tracking[tracking["player_id"] == "home-10"]
    replaced = tracking[
        (tracking["player_id"] == "home-09") & (tracking["period"] == 2)
    ]

    assert set(substitute["period"]) == {2}
    assert substitute["timestamp_seconds"].min() > 90
    assert replaced["timestamp_seconds"].max() == 90


@pytest.mark.parametrize("seed", [42, 20_250_714, 20_260_720])
def test_synthetic_match_contains_plausible_sprint_bouts(seed: int) -> None:
    tracking = generate_synthetic_match(seed=seed, period_duration_s=40).tracking
    sprints = detect_sprints(tracking)

    assert not sprints.empty
    assert sprints["peak_speed_mps"].max() <= 12.5
