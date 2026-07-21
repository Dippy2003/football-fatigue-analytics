"""Coordinate conversions into the 105 x 68 metre canonical pitch."""

from __future__ import annotations

from typing import Literal

import pandas as pd

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG

CoordinateSystem = Literal["metres", "normalized", "statsbomb"]


def convert_xy(
    frame: pd.DataFrame,
    *,
    x_column: str,
    y_column: str,
    system: CoordinateSystem,
) -> pd.DataFrame:
    """Convert a coordinate pair while preserving null locations."""
    converted = frame.copy()
    if system == "metres":
        x_scale, y_scale = 1.0, 1.0
    elif system == "normalized":
        x_scale = DEFAULT_ANALYTICS_CONFIG.pitch_length_m
        y_scale = DEFAULT_ANALYTICS_CONFIG.pitch_width_m
    else:
        x_scale = DEFAULT_ANALYTICS_CONFIG.pitch_length_m / 120
        y_scale = DEFAULT_ANALYTICS_CONFIG.pitch_width_m / 80
    converted[x_column] = pd.to_numeric(converted[x_column]) * x_scale
    converted[y_column] = pd.to_numeric(converted[y_column]) * y_scale
    return converted


def validate_pitch_bounds(
    frame: pd.DataFrame, *, coordinate_pairs: tuple[tuple[str, str], ...]
) -> None:
    """Reject finite coordinates outside the canonical pitch."""
    for x_column, y_column in coordinate_pairs:
        invalid = (
            frame[x_column].notna()
            & frame[y_column].notna()
            & (
                ~frame[x_column].between(0, DEFAULT_ANALYTICS_CONFIG.pitch_length_m)
                | ~frame[y_column].between(0, DEFAULT_ANALYTICS_CONFIG.pitch_width_m)
            )
        )
        if invalid.any():
            raise ValueError(
                f"coordinates outside pitch bounds: {x_column}, {y_column}"
            )
