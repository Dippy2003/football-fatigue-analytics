"""Tests use generated CSVs, never redistributed Metrica data."""

from pathlib import Path

import pandas as pd
import pytest

from app.data.importers.metrica import load_metrica_events, load_metrica_tracking


def test_metrica_tracking_converts_normalized_coordinates(tmp_path: Path) -> None:
    path = tmp_path / "developer-supplied.csv"
    pd.DataFrame(
        {
            "match_id": ["local-1"],
            "period": [1],
            "frame_id": [1],
            "timestamp_seconds": [0.04],
            "team_id": ["Home"],
            "player_id": ["Home_1"],
            "x": [0.5],
            "y": [0.5],
            "ball_x": [1.0],
            "ball_y": [1.0],
        }
    ).to_csv(path, index=False)

    result = load_metrica_tracking(path)

    assert (result.loc[0, "x"], result.loc[0, "y"]) == (52.5, 34.0)
    assert result.loc[0, "source"] == "metrica_sample_data"
    assert not bool(result.loc[0, "is_synthetic"])


def test_metrica_tracking_rejects_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.csv"
    pd.DataFrame({"x": [0.5]}).to_csv(path, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_metrica_tracking(path)


def test_metrica_tracking_requires_existing_local_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_metrica_tracking(tmp_path / "not-downloaded.csv")


def test_metrica_events_convert_locations(tmp_path: Path) -> None:
    path = tmp_path / "developer-events.csv"
    pd.DataFrame(
        {
            "match_id": ["local-1"],
            "event_id": ["event-1"],
            "period": [1],
            "timestamp_seconds": [12.0],
            "team_id": ["Home"],
            "event_type": ["PASS"],
            "start_x": [0.25],
            "start_y": [0.5],
            "end_x": [0.75],
            "end_y": [0.5],
        }
    ).to_csv(path, index=False)

    result = load_metrica_events(path)

    assert result.loc[0, "start_x"] == 26.25
    assert result.loc[0, "end_x"] == 78.75
    assert result.loc[0, "source"] == "metrica_sample_data"
