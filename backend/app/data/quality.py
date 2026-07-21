"""Transparent match and player data-quality scoring."""

from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

from app.analytics.movement import flag_physiological_outliers


class QualityReport(BaseModel):
    """Bounded evidence about analytical input reliability."""

    model_config = ConfigDict(extra="forbid")

    row_count: int = Field(ge=0)
    coordinate_completeness: float = Field(ge=0, le=1)
    timestamp_monotonicity: float = Field(ge=0, le=1)
    plausible_speed_rate: float = Field(ge=0, le=1)
    quality_score: float = Field(ge=0, le=100)
    confidence: str
    limitations: list[str]


def build_quality_report(frame: pd.DataFrame) -> QualityReport:
    """Calculate a documented weighted quality score for tracking data."""
    if frame.empty:
        return QualityReport(
            row_count=0,
            coordinate_completeness=0,
            timestamp_monotonicity=0,
            plausible_speed_rate=0,
            quality_score=0,
            confidence="unavailable",
            limitations=["No tracking observations were supplied."],
        )
    completeness = float((~frame[["x", "y"]].isna().any(axis=1)).mean())
    deltas = (
        frame.sort_values(["match_id", "period", "player_id", "timestamp_seconds"])
        .groupby(["match_id", "period", "player_id"])["timestamp_seconds"]
        .diff()
    )
    timestamp_monotonicity = (
        float((deltas.dropna() > 0).mean()) if deltas.notna().any() else 1.0
    )
    enriched = flag_physiological_outliers(frame)
    observed_speeds = enriched["speed_mps"].notna()
    plausible_rate = (
        float((~enriched.loc[observed_speeds, "is_speed_outlier"]).mean())
        if observed_speeds.any()
        else 0.0
    )
    score = round(
        100
        * (0.5 * completeness + 0.2 * timestamp_monotonicity + 0.3 * plausible_rate),
        1,
    )
    limitations: list[str] = []
    if completeness < 1:
        limitations.append("Some player coordinates are missing.")
    if plausible_rate < 1:
        limitations.append(
            "Some speed observations exceed the configured plausible limit."
        )
    confidence = "high" if score >= 90 else "moderate" if score >= 70 else "low"
    return QualityReport(
        row_count=len(frame),
        coordinate_completeness=completeness,
        timestamp_monotonicity=timestamp_monotonicity,
        plausible_speed_rate=plausible_rate,
        quality_score=score,
        confidence=confidence,
        limitations=limitations,
    )
