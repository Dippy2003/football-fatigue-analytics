"""Transparent player workload baseline selection."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev


@dataclass(frozen=True)
class BaselineResult:
    """Selected comparison population and workload z-score."""

    baseline_type: str
    confidence: float
    sample_size: int
    mean_workload: float
    standard_deviation: float
    workload_zscore: float


def _summarize(
    current_workload: float,
    values: list[float],
    *,
    baseline_type: str,
    confidence: float,
) -> BaselineResult:
    mean = fmean(values)
    deviation = pstdev(values)
    zscore = (current_workload - mean) / deviation if deviation > 0 else 0.0
    return BaselineResult(
        baseline_type=baseline_type,
        confidence=confidence,
        sample_size=len(values),
        mean_workload=mean,
        standard_deviation=deviation,
        workload_zscore=zscore,
    )


def select_workload_baseline(
    *,
    current_workload: float,
    personal_history: list[float],
    comparable_team_history: list[float],
    early_match_workload: float | None = None,
) -> BaselineResult | None:
    """Choose personal, comparable-team, then match-only evidence."""
    if len(personal_history) >= 5:
        return _summarize(
            current_workload,
            personal_history,
            baseline_type="personal_historical",
            confidence=1.0,
        )
    if len(personal_history) >= 3:
        return _summarize(
            current_workload,
            personal_history,
            baseline_type="personal_historical_limited",
            confidence=0.8,
        )
    if len(comparable_team_history) >= 10:
        return _summarize(
            current_workload,
            comparable_team_history,
            baseline_type="position_team",
            confidence=0.65,
        )
    if early_match_workload is not None and early_match_workload > 0:
        return BaselineResult(
            baseline_type="match_only",
            confidence=0.4,
            sample_size=1,
            mean_workload=early_match_workload,
            standard_deviation=0,
            workload_zscore=0,
        )
    return None
