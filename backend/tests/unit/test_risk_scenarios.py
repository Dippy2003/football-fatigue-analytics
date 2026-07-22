"""Logical synthetic risk and threshold sensitivity scenarios."""

import pytest

from app.analytics.risk import RiskInputs, calculate_risk, piecewise


@pytest.mark.parametrize(
    ("value", "expected"),
    [(4.999, 0), (5.0, 0), (5.001, pytest.approx(0.003333, abs=1e-5)), (35, 100)],
)
def test_speed_decline_boundary_sensitivity(value: float, expected: object) -> None:
    assert piecewise(value, zero_at=5, full_at=35) == expected


def test_high_workload_without_decline_is_not_forced_high() -> None:
    result = calculate_risk(
        RiskInputs(
            speed_decline_pct=0,
            sprint_frequency_decline_pct=0,
            sprint_recovery_increase_pct=0,
            workload_vs_baseline_zscore=2,
            data_quality=1,
            baseline_confidence=1,
        ),
        baseline_type="personal_historical",
    )

    assert result.score is not None and result.score < 30
    assert result.category == "Low indicator level"


def test_severe_decline_scenario_reaches_very_high_indicator() -> None:
    result = calculate_risk(
        RiskInputs(
            speed_decline_pct=35,
            sprint_frequency_decline_pct=60,
            sprint_recovery_increase_pct=80,
            workload_vs_baseline_zscore=3,
            event_performance_decline_pct=50,
            data_quality=1,
            baseline_confidence=1,
        ),
        baseline_type="personal_historical",
    )

    assert result.score == 100
    assert result.category == "Very high indicator level"
    assert result.confidence == 1


def test_two_core_factors_cannot_issue_numeric_score() -> None:
    result = calculate_risk(
        RiskInputs(
            speed_decline_pct=20,
            sprint_frequency_decline_pct=30,
            event_performance_decline_pct=20,
            data_quality=1,
            baseline_confidence=0.65,
        ),
        baseline_type="position_team",
    )

    assert result.assessment_status == "insufficient_data"
    assert "Fewer than three core physical factors" in result.limitations[0]
