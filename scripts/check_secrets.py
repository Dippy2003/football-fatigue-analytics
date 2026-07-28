"""Detect high-confidence credential material in tracked text files."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path("scripts/check_secrets.py")
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}


def tracked_files() -> list[Path]:
    """Return Git-tracked paths without inspecting ignored local secrets."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [Path(raw.decode()) for raw in result.stdout.split(b"\0") if raw]


def violations(paths: list[Path]) -> list[str]:
    """Return high-confidence secret matches with file and pattern names."""
    failures: list[str] = []
    for relative in paths:
        absolute = ROOT / relative
        if (
            relative == SELF
            or relative.suffix.casefold() not in TEXT_SUFFIXES
            or not absolute.is_file()
        ):
            continue
        content = absolute.read_text(encoding="utf-8", errors="replace")
        for name, pattern in PATTERNS.items():
            if pattern.search(content):
                failures.append(f"{relative}: possible {name}")
    return failures


def main() -> int:
    """Fail the release when tracked credential material is detected."""
    failures = violations(tracked_files())
    if failures:
        print("PlayerPulse tracked-secret check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PlayerPulse tracked-secret check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
