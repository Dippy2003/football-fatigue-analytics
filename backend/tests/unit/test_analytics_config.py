"""Analytics configuration tests."""

import pytest
from pydantic import ValidationError

from app.analytics.config import DEFAULT_ANALYTICS_CONFIG, AnalyticsConfig


def test_defaults_match_documented_pitch_and_thresholds() -> None:
    config = DEFAULT_ANALYTICS_CONFIG

    assert (config.pitch_length_m, config.pitch_width_m) == (105.0, 68.0)
    assert config.intensity_zone_edges_mps == (2.0, 4.0, 5.5, 7.0)
    assert config.sprint_min_duration_s == 0.5


def test_zone_edges_must_be_strictly_ordered() -> None:
    with pytest.raises(ValidationError, match="strictly ordered"):
        AnalyticsConfig(intensity_zone_edges_mps=(2.0, 5.5, 4.0, 7.0))
