"""Canonical, provider-neutral football data schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TrackingRecord(BaseModel):
    """One canonical player tracking observation in pitch metres."""

    model_config = ConfigDict(extra="forbid")

    match_id: str
    period: int = Field(ge=1)
    frame_id: int = Field(ge=0)
    timestamp_seconds: float = Field(ge=0)
    team_id: str
    player_id: str
    x: float = Field(ge=0, le=105)
    y: float = Field(ge=0, le=68)
    ball_x: float | None = Field(default=None, ge=0, le=105)
    ball_y: float | None = Field(default=None, ge=0, le=68)
    source: str
    is_synthetic: bool


class EventRecord(BaseModel):
    """One canonical on-ball or defensive event in pitch metres."""

    model_config = ConfigDict(extra="forbid")

    match_id: str
    event_id: str
    period: int = Field(ge=1)
    timestamp_seconds: float = Field(ge=0)
    team_id: str
    player_id: str | None = None
    event_type: str
    outcome: str | None = None
    start_x: float = Field(ge=0, le=105)
    start_y: float = Field(ge=0, le=68)
    end_x: float | None = Field(default=None, ge=0, le=105)
    end_y: float | None = Field(default=None, ge=0, le=68)
    source: str
    is_synthetic: bool

    @model_validator(mode="after")
    def require_complete_end_location(self) -> EventRecord:
        """Prevent half-specified event destinations."""
        if (self.end_x is None) != (self.end_y is None):
            raise ValueError("event end_x and end_y must be provided together")
        return self


class DataQualityFlag(BaseModel):
    """Structured quality issue emitted by ingestion and cleaning."""

    model_config = ConfigDict(extra="forbid")

    code: str
    severity: Literal["info", "warning", "error"]
    message: str
    row_count: int = Field(default=0, ge=0)
