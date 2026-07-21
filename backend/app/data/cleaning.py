"""Canonical tracking cleaning with auditable quality flags."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG
from app.data.schemas import DataQualityFlag

TRACKING_KEY = ["match_id", "period", "player_id", "timestamp_seconds"]
TRACKING_ORDER = ["match_id", "period", "timestamp_seconds", "player_id"]


@dataclass(frozen=True)
class CleaningResult:
    """Cleaned rows plus non-destructive quality evidence."""

    frame: pd.DataFrame
    flags: tuple[DataQualityFlag, ...]


def sort_and_deduplicate_tracking(frame: pd.DataFrame) -> CleaningResult:
    """Sort deterministically and keep the first duplicate observation."""
    duplicate_mask = frame.duplicated(subset=TRACKING_KEY, keep="first")
    duplicate_count = int(duplicate_mask.sum())
    cleaned = frame.loc[~duplicate_mask].sort_values(
        TRACKING_ORDER, kind="stable", ignore_index=True
    )
    flags: list[DataQualityFlag] = []
    if duplicate_count:
        flags.append(
            DataQualityFlag(
                code="duplicate_tracking_rows_removed",
                severity="warning",
                message="Duplicate player observations were removed.",
                row_count=duplicate_count,
            )
        )
    return CleaningResult(frame=cleaned, flags=tuple(flags))


def interpolate_short_tracking_gaps(
    frame: pd.DataFrame,
    *,
    max_gap_s: float = DEFAULT_ANALYTICS_CONFIG.interpolation_max_gap_s,
) -> CleaningResult:
    """Linearly fill short internal x/y gaps inside player-period groups."""
    cleaned = frame.copy()
    cleaned["was_interpolated"] = False
    filled_count = 0
    group_columns = ["match_id", "period", "player_id"]
    for _, indexes in cleaned.groupby(group_columns, sort=False).groups.items():
        group = cleaned.loc[indexes].sort_values("timestamp_seconds")
        for column in ("x", "y"):
            missing = group[column].isna()
            candidate = group[column].interpolate(method="linear", limit_area="inside")
            previous_time = group["timestamp_seconds"].where(~missing).ffill()
            next_time = group["timestamp_seconds"].where(~missing).bfill()
            short_gap = missing & ((next_time - previous_time) <= max_gap_s)
            target_indexes = group.index[short_gap]
            cleaned.loc[target_indexes, column] = candidate.loc[target_indexes]
            cleaned.loc[target_indexes, "was_interpolated"] = True
            filled_count += int(short_gap.sum())
    flags: list[DataQualityFlag] = []
    if filled_count:
        flags.append(
            DataQualityFlag(
                code="short_tracking_gaps_interpolated",
                severity="info",
                message="Short internal coordinate gaps were linearly interpolated.",
                row_count=filled_count,
            )
        )
    remaining = int(cleaned[["x", "y"]].isna().any(axis=1).sum())
    if remaining:
        flags.append(
            DataQualityFlag(
                code="tracking_gaps_unresolved",
                severity="warning",
                message="Long or boundary coordinate gaps remain unresolved.",
                row_count=remaining,
            )
        )
    return CleaningResult(frame=cleaned, flags=tuple(flags))
