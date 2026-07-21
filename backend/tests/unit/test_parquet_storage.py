"""Parquet output tests use temporary synthetic tables."""

from pathlib import Path

import pandas as pd
import pytest

from app.data.storage import read_match_parquet, write_match_parquet


def test_parquet_round_trip_preserves_table(tmp_path: Path) -> None:
    original = pd.DataFrame(
        {"match_id": ["synthetic-match-001"], "distance_m": [123.4]}
    )

    paths = write_match_parquet(
        tmp_path,
        match_id="synthetic-match-001",
        tables={"player_metrics": original},
    )

    assert paths["player_metrics"].suffix == ".parquet"
    pd.testing.assert_frame_equal(read_match_parquet(paths["player_metrics"]), original)


@pytest.mark.parametrize("match_id", ["", "../escape", "folder/name"])
def test_parquet_writer_rejects_unsafe_match_ids(tmp_path: Path, match_id: str) -> None:
    with pytest.raises(ValueError, match="safe filename"):
        write_match_parquet(tmp_path, match_id=match_id, tables={})


def test_parquet_reader_rejects_pickle_extension(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="only Parquet"):
        read_match_parquet(tmp_path / "unsafe.pkl")
