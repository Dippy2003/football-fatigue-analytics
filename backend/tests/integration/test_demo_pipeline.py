"""Synthetic demo pipeline integration test."""

from pathlib import Path

from app.data.processing import process_synthetic_demo
from app.data.storage import read_match_parquet


def test_demo_pipeline_cleans_analyzes_and_writes_parquet(tmp_path: Path) -> None:
    result = process_synthetic_demo(
        output_directory=tmp_path, seed=42, period_duration_s=10
    )

    assert set(result.tables) == {
        "tracking",
        "movement_features",
        "sprints",
        "match_windows",
        "event_metrics",
        "events",
    }
    assert not result.tables["tracking"][["x", "y"]].isna().any().any()
    assert result.quality.confidence == "high"
    assert len(result.output_paths) == 6
    stored = read_match_parquet(result.output_paths["movement_features"])
    assert "intensity_zone" in stored.columns
    assert stored["is_synthetic"].all()
