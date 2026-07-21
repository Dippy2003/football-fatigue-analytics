"""Parquet persistence for canonical and derived match tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_match_parquet(
    output_directory: Path, *, match_id: str, tables: dict[str, pd.DataFrame]
) -> dict[str, Path]:
    """Write named tables with deterministic filenames and no pickle fallback."""
    if not match_id or any(character in match_id for character in ("/", "\\", "..")):
        raise ValueError("match_id must be a safe filename component")
    output_directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, table in sorted(tables.items()):
        if not name.replace("_", "").isalnum():
            raise ValueError(f"unsafe table name: {name}")
        path = output_directory / f"{match_id}.{name}.parquet"
        table.to_parquet(path, engine="pyarrow", index=False)
        paths[name] = path
    return paths


def read_match_parquet(path: Path) -> pd.DataFrame:
    """Read a Parquet table without unsafe object deserialization."""
    if path.suffix.lower() != ".parquet":
        raise ValueError("only Parquet analytics tables are supported")
    return pd.read_parquet(path, engine="pyarrow")
