"""End-to-end deterministic demo processing pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from app.analytics.events import summarize_event_metrics
from app.analytics.intensity import classify_intensity_zones
from app.analytics.movement import add_acceleration_features
from app.analytics.sprints import detect_sprints
from app.analytics.windows import summarize_match_windows
from app.data.cleaning import (
    interpolate_short_tracking_gaps,
    sort_and_deduplicate_tracking,
)
from app.data.quality import QualityReport, build_quality_report
from app.data.storage import write_match_parquet
from app.data.synthetic import generate_synthetic_match


@dataclass(frozen=True)
class ProcessingResult:
    """Derived tables and quality evidence from one match."""

    tables: dict[str, pd.DataFrame]
    quality: QualityReport
    output_paths: dict[str, Path]


def process_synthetic_demo(
    *,
    output_directory: Path | None = None,
    seed: int = 20250714,
    period_duration_s: int = 180,
) -> ProcessingResult:
    """Run canonical cleaning and analytics using only fictional data."""
    match = generate_synthetic_match(seed=seed, period_duration_s=period_duration_s)
    ordered = sort_and_deduplicate_tracking(match.tracking)
    interpolated = interpolate_short_tracking_gaps(ordered.frame)
    movement = add_acceleration_features(interpolated.frame)
    intensity = classify_intensity_zones(interpolated.frame)
    movement["intensity_zone"] = intensity["intensity_zone"]
    tables = {
        "tracking": interpolated.frame,
        "movement_features": movement,
        "sprints": detect_sprints(interpolated.frame),
        "match_windows": summarize_match_windows(interpolated.frame),
        "event_metrics": summarize_event_metrics(match.events),
        "events": match.events,
    }
    quality = build_quality_report(interpolated.frame)
    output_paths = (
        write_match_parquet(
            output_directory, match_id="synthetic-match-001", tables=tables
        )
        if output_directory is not None
        else {}
    )
    return ProcessingResult(tables=tables, quality=quality, output_paths=output_paths)
