"""Deterministic explainable performance-risk indicator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

DISCLAIMER = (
    "PlayerPulse provides performance-based indicators from available match data. "
    "It is not a medical diagnostic tool and must not be used as a substitute for "
    "qualified medical or sports-science assessment."
)
MODEL_VERSION = "rule-risk-v1"
WEIGHTS = {
    "speed_decline": 0.25,
    "sprint_frequency_decline": 0.25,
    "sprint_recovery_increase": 0.20,
    "workload_vs_baseline": 0.20,
    "event_performance_decline": 0.10,
}
CORE_FACTORS = {
    "speed_decline",
    "sprint_frequency_decline",
    "sprint_recovery_increase",
    "workload_vs_baseline",
}


@dataclass(frozen=True)
class RiskInputs:
    """Raw percentage/z-score inputs; missing evidence stays missing."""

    speed_decline_pct: float | None = None
    sprint_frequency_decline_pct: float | None = None
    sprint_recovery_increase_pct: float | None = None
    workload_vs_baseline_zscore: float | None = None
    event_performance_decline_pct: float | None = None
    data_quality: float = 0
    baseline_confidence: float = 0


@dataclass(frozen=True)
class FactorContribution:
    """One normalized factor and its effective weighted contribution."""

    factor: str
    raw_value: float
    normalized_score: float
    effective_weight: float
    contribution: float


@dataclass(frozen=True)
class RiskResult:
    """Complete risk response independent of transport or persistence."""

    assessment_status: str
    score: float | None
    category: str | None
    confidence: float
    data_quality: float
    feature_coverage: float
    baseline_type: str
    factors: tuple[FactorContribution, ...]
    top_contributing_factors: tuple[str, ...]
    explanation: str
    limitations: tuple[str, ...]
    disclaimer: str
    model_version: str
    calculated_at: datetime


def piecewise(value: float, *, zero_at: float, full_at: float) -> float:
    """Clamp a linear factor score to 0..100."""
    if value <= zero_at:
        return 0.0
    if value >= full_at:
        return 100.0
    return 100 * (value - zero_at) / (full_at - zero_at)


def _factors(inputs: RiskInputs) -> dict[str, tuple[float, float]]:
    values: dict[str, tuple[float, float]] = {}
    mappings = (
        ("speed_decline", inputs.speed_decline_pct, 5.0, 35.0),
        ("sprint_frequency_decline", inputs.sprint_frequency_decline_pct, 10.0, 60.0),
        ("sprint_recovery_increase", inputs.sprint_recovery_increase_pct, 10.0, 80.0),
        ("workload_vs_baseline", inputs.workload_vs_baseline_zscore, 1.0, 3.0),
        ("event_performance_decline", inputs.event_performance_decline_pct, 5.0, 50.0),
    )
    for name, raw, zero_at, full_at in mappings:
        if raw is not None:
            values[name] = (raw, piecewise(raw, zero_at=zero_at, full_at=full_at))
    return values


def calculate_risk(inputs: RiskInputs, *, baseline_type: str) -> RiskResult:
    """Calculate a deterministic score or an honest insufficient-data state."""
    factors = _factors(inputs)
    coverage = len(factors) / len(WEIGHTS)
    core_count = len(CORE_FACTORS.intersection(factors))
    confidence = max(
        0,
        min(
            1,
            0.5 * inputs.data_quality
            + 0.35 * inputs.baseline_confidence
            + 0.15 * coverage,
        ),
    )
    limitations: list[str] = []
    if inputs.data_quality < 0.5:
        limitations.append("Data quality is below the 0.50 availability threshold.")
    if core_count < 3:
        limitations.append("Fewer than three core physical factors are available.")
    if coverage < 0.6:
        limitations.append("Feature coverage is below 60%.")
    if limitations:
        return RiskResult(
            assessment_status="insufficient_data",
            score=None,
            category=None,
            confidence=confidence,
            data_quality=inputs.data_quality,
            feature_coverage=coverage,
            baseline_type=baseline_type,
            factors=(),
            top_contributing_factors=(),
            explanation="A numeric performance-risk indicator was not issued.",
            limitations=tuple(limitations),
            disclaimer=DISCLAIMER,
            model_version=MODEL_VERSION,
            calculated_at=datetime.now(UTC),
        )
    available_weight = sum(WEIGHTS[name] for name in factors)
    contributions = tuple(
        FactorContribution(
            factor=name,
            raw_value=raw,
            normalized_score=normalized,
            effective_weight=WEIGHTS[name] / available_weight,
            contribution=normalized * WEIGHTS[name] / available_weight,
        )
        for name, (raw, normalized) in factors.items()
    )
    score = round(sum(item.contribution for item in contributions), 1)
    category = (
        "Low indicator level"
        if score <= 30
        else "Moderate indicator level"
        if score <= 60
        else "High indicator level"
        if score <= 80
        else "Very high indicator level"
    )
    ranked = sorted(contributions, key=lambda item: item.contribution, reverse=True)
    top = tuple(item.factor for item in ranked[:3])
    return RiskResult(
        assessment_status="available",
        score=score,
        category=category,
        confidence=confidence,
        data_quality=inputs.data_quality,
        feature_coverage=coverage,
        baseline_type=baseline_type,
        factors=contributions,
        top_contributing_factors=top,
        explanation=(
            f"{category}. The largest available contribution is "
            f"{top[0].replace('_', ' ')}. "
            "Review workload and recovery context with qualified staff."
        ),
        limitations=(),
        disclaimer=DISCLAIMER,
        model_version=MODEL_VERSION,
        calculated_at=datetime.now(UTC),
    )
