"""Canonical data schema tests."""

import pytest
from pydantic import ValidationError

from app.data.schemas import EventRecord, TrackingRecord


def tracking_payload() -> dict[str, object]:
    return {
        "match_id": "synthetic-match-001",
        "period": 1,
        "frame_id": 10,
        "timestamp_seconds": 1.0,
        "team_id": "home",
        "player_id": "home-01",
        "x": 52.5,
        "y": 34.0,
        "ball_x": 50.0,
        "ball_y": 33.0,
        "source": "synthetic_playerpulse",
        "is_synthetic": True,
    }


def test_tracking_record_accepts_pitch_coordinates() -> None:
    record = TrackingRecord.model_validate(tracking_payload())

    assert record.x == 52.5
    assert record.is_synthetic


def test_tracking_record_rejects_out_of_bounds_coordinate() -> None:
    payload = tracking_payload()
    payload["x"] = 106.0

    with pytest.raises(ValidationError, match="less than or equal to 105"):
        TrackingRecord.model_validate(payload)


def test_event_destination_must_be_complete() -> None:
    with pytest.raises(ValidationError, match="provided together"):
        EventRecord(
            match_id="synthetic-match-001",
            event_id="evt-1",
            period=1,
            timestamp_seconds=2.0,
            team_id="home",
            event_type="pass",
            start_x=30,
            start_y=20,
            end_x=40,
            source="synthetic_playerpulse",
            is_synthetic=True,
        )
