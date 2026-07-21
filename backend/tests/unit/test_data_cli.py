"""Data CLI tests."""

import json
from pathlib import Path

import pytest

from app.cli import main


def test_generate_demo_cli_writes_parquet_and_summary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [
            "generate-demo",
            "--output",
            str(tmp_path),
            "--seed",
            "42",
            "--period-duration",
            "10",
        ]
    )
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["is_synthetic"] is True
    assert payload["quality"]["confidence"] == "high"
    assert len(list(tmp_path.glob("*.parquet"))) == 6
