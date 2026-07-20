"""Fail when tracked files violate PlayerPulse data-distribution rules."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_DIRECTORIES = (
    Path("data/raw"),
    Path("data/interim"),
    Path("data/processed"),
)
PROHIBITED_MODEL_SUFFIXES = {".joblib", ".pickle", ".pkl"}
MAX_TRACKED_FILE_BYTES = 10 * 1024 * 1024


def tracked_files() -> list[Path]:
    """Return repository paths tracked by Git."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def violations(paths: list[Path]) -> list[str]:
    """Describe tracked files that are unsafe to distribute."""
    failures: list[str] = []
    for relative_path in paths:
        absolute_path = ROOT / relative_path
        if not absolute_path.is_file():
            continue

        if (
            any(
                relative_path.is_relative_to(directory)
                for directory in PROTECTED_DIRECTORIES
            )
            and relative_path.name != ".gitkeep"
        ):
            failures.append(f"generated or raw data is tracked: {relative_path}")

        if relative_path.suffix.casefold() in PROHIBITED_MODEL_SUFFIXES:
            failures.append(f"binary model artifact is tracked: {relative_path}")

        if absolute_path.stat().st_size > MAX_TRACKED_FILE_BYTES:
            failures.append(f"tracked file exceeds 10 MiB: {relative_path}")

    return failures


def main() -> int:
    """Run repository data-distribution checks."""
    failures = violations(tracked_files())
    if failures:
        print("PlayerPulse dataset-file check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PlayerPulse dataset-file check passed: no prohibited tracked data found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
