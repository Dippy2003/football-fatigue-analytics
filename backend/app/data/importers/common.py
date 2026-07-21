"""Shared importer validation helpers."""

from pathlib import Path

import pandas as pd


def require_local_file(path: Path) -> Path:
    """Require an existing regular file supplied by the developer."""
    resolved = path.resolve(strict=True)
    if not resolved.is_file():
        raise ValueError(f"import path is not a regular file: {resolved}")
    return resolved


def require_columns(frame: pd.DataFrame, required: set[str]) -> None:
    """Reject incomplete provider tables with a useful field list."""
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
