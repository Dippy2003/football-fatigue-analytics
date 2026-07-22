"""Rule-based risk scoring tests."""

from app.analytics.risk import DISCLAIMER, RiskInputs, calculate_risk, piecewise


def test_piecewise_scaling_clamps_thresholds() -> None:
    assert piecewise(5, zero_at=5, full_at=35) == 0
    assert piecewise(20, zero_at=5, full_at=35) == 50
    assert piecewise(35, zero_at=5, full_at=35) == 100


def test_available_result_renormalizes_missing_event_factor() -> None:
    result = calculate_risk(
        RiskInputs(
            speed_decline_pct=20,
            sprint_frequency_decline_pct=35,
            sprint_recovery_increase_pct=45,
            workload_vs_baseline_zscore=2,
            data_quality=1,
            baseline_confidence=0.8,
        ),
        baseline_type="personal_historical_limited",
    )

    assert result.assessment_status == "available"
    assert result.score == 50
    assert sum(item.effective_weight for item in result.factors) == 1
    assert result.disclaimer == DISCLAIMER


def test_low_quality_returns_insufficient_data_not_low_score() -> None:
    result = calculate_risk(
        RiskInputs(
            speed_decline_pct=35,
            sprint_frequency_decline_pct=60,
            sprint_recovery_increase_pct=80,
            data_quality=0.49,
            baseline_confidence=1,
        ),
        baseline_type="personal_historical",
    )

    assert result.assessment_status == "insufficient_data"
    assert result.score is None
    assert result.category is None
