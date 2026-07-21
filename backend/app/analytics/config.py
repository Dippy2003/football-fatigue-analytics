"""Typed defaults for provider-neutral football analytics."""

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AnalyticsConfig(BaseModel):
    """Validated thresholds used by cleaning and feature extraction."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pitch_length_m: float = Field(default=105.0, gt=0)
    pitch_width_m: float = Field(default=68.0, gt=0)
    interpolation_max_gap_s: float = Field(default=0.5, ge=0)
    physiological_max_speed_mps: float = Field(default=12.5, gt=0)
    smoothing_window_s: float = Field(default=0.2, gt=0)
    intensity_zone_edges_mps: tuple[float, float, float, float] = (
        2.0,
        4.0,
        5.5,
        7.0,
    )
    sprint_min_duration_s: float = Field(default=0.5, gt=0)
    sprint_merge_gap_s: float = Field(default=0.2, ge=0)
    event_sync_tolerance_s: float = Field(default=0.1, ge=0)
    window_minutes: int = Field(default=15, gt=0)

    @model_validator(mode="after")
    def require_ordered_zone_edges(self) -> "AnalyticsConfig":
        """Ensure intensity bands cannot overlap or reverse."""
        if (
            tuple(sorted(self.intensity_zone_edges_mps))
            != self.intensity_zone_edges_mps
        ):
            raise ValueError("intensity zone edges must be strictly ordered")
        if len(set(self.intensity_zone_edges_mps)) != 4:
            raise ValueError("intensity zone edges must be unique")
        return self


DEFAULT_ANALYTICS_CONFIG = AnalyticsConfig()
