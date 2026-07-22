"""Baseline selection tests."""

from app.analytics.baselines import select_workload_baseline


def test_personal_history_has_priority_and_full_confidence() -> None:
    result = select_workload_baseline(
        current_workload=120,
        personal_history=[90, 95, 100, 105, 110],
        comparable_team_history=[100] * 10,
    )

    assert result is not None
    assert result.baseline_type == "personal_historical"
    assert result.confidence == 1
    assert result.workload_zscore > 0


def test_team_and_match_only_fallbacks_are_explicit() -> None:
    team_result = select_workload_baseline(
        current_workload=110,
        personal_history=[],
        comparable_team_history=[100] * 10,
    )
    match_result = select_workload_baseline(
        current_workload=110,
        personal_history=[],
        comparable_team_history=[],
        early_match_workload=100,
    )

    assert team_result is not None and team_result.confidence == 0.65
    assert match_result is not None and match_result.confidence == 0.4


def test_insufficient_comparison_data_returns_none() -> None:
    assert (
        select_workload_baseline(
            current_workload=100,
            personal_history=[90, 95],
            comparable_team_history=[100] * 9,
        )
        is None
    )
