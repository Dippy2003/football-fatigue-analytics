"""StatsBomb adapter tests use tiny fictional JSON fixtures."""

import json
from pathlib import Path

import pytest

from app.data.importers.statsbomb import load_statsbomb_events


def write_fixture(path: Path) -> None:
    path.write_text(
        json.dumps(
            [
                {
                    "id": "fictional-1",
                    "period": 1,
                    "minute": 2,
                    "second": 3,
                    "team": {"id": 1},
                    "player": {"id": 10},
                    "type": {"name": "Pass"},
                    "location": [60, 40],
                    "pass": {"end_location": [120, 80]},
                }
            ]
        ),
        encoding="utf-8",
    )


def test_statsbomb_adapter_fails_closed_without_acknowledgement(tmp_path: Path) -> None:
    path = tmp_path / "events.json"
    write_fixture(path)

    with pytest.raises(PermissionError, match="current terms"):
        load_statsbomb_events(path, match_id="local-1")


def test_statsbomb_adapter_maps_event_and_coordinates(tmp_path: Path) -> None:
    path = tmp_path / "events.json"
    write_fixture(path)

    result = load_statsbomb_events(path, match_id="local-1", rights_acknowledged=True)

    assert result.loc[0, "timestamp_seconds"] == 123
    assert (result.loc[0, "start_x"], result.loc[0, "start_y"]) == (52.5, 34.0)
    assert (result.loc[0, "end_x"], result.loc[0, "end_y"]) == (105.0, 68.0)
