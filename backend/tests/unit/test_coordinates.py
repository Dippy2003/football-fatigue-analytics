"""Coordinate conversion tests."""

import pandas as pd
import pytest

from app.data.coordinates import convert_xy, validate_pitch_bounds


@pytest.mark.parametrize(
    ("system", "source", "expected"),
    [
        ("metres", (105.0, 68.0), (105.0, 68.0)),
        ("normalized", (1.0, 1.0), (105.0, 68.0)),
        ("statsbomb", (120.0, 80.0), (105.0, 68.0)),
    ],
)
def test_coordinate_boundaries_convert_exactly(
    system: str, source: tuple[float, float], expected: tuple[float, float]
) -> None:
    frame = pd.DataFrame({"x": [source[0]], "y": [source[1]]})

    result = convert_xy(frame, x_column="x", y_column="y", system=system)  # type: ignore[arg-type]

    assert (result.loc[0, "x"], result.loc[0, "y"]) == expected


def test_pitch_bounds_reject_negative_values() -> None:
    frame = pd.DataFrame({"x": [-0.1], "y": [34.0]})

    with pytest.raises(ValueError, match="outside pitch bounds"):
        validate_pitch_bounds(frame, coordinate_pairs=(("x", "y"),))


def test_conversion_preserves_missing_coordinates() -> None:
    result = convert_xy(
        pd.DataFrame({"x": [None], "y": [None]}),
        x_column="x",
        y_column="y",
        system="normalized",
    )

    assert result[["x", "y"]].isna().all().all()
