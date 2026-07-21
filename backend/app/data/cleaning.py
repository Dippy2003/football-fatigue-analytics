"""Canonical tracking cleaning with auditable quality flags."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

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
