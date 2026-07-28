"""Verify release-critical files, versions, wording, and repository hygiene."""

from __future__ import annotations

import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
DISCLAIMER = (
    "PlayerPulse provides performance-based indicators from available match data. "
    "It is not a medical diagnostic tool and must not be used as a substitute for "
    "qualified medical or sports-science assessment."
)
REQUIRED_DOCS = (
    "README.md",
    "SECURITY.md",
    "docs/API.md",
    "docs/ARCHITECTURE.md",
    "docs/DATASET_ATTRIBUTION.md",
    "docs/DATA_CARD.md",
    "docs/DATA_DICTIONARY.md",
    "docs/DEPLOYMENT.md",
    "docs/ETHICS_AND_LIMITATIONS.md",
    "docs/METHODOLOGY.md",
    "docs/MODEL_CARD.md",
    "docs/RELEASE_CHECKLIST.md",
    "docs/TESTING.md",
    "docs/USER_GUIDE.md",
)


def git_output(*args: str) -> str:
    """Return stripped Git output for a release assertion."""
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def collect_failures(*, require_tags: bool = False) -> list[str]:
    """Collect release blockers without stopping at the first failure."""
    failures = [
        f"missing required file: {path}"
        for path in REQUIRED_DOCS
        if not (ROOT / path).is_file()
    ]
    with (ROOT / "backend/pyproject.toml").open("rb") as stream:
        backend_version = tomllib.load(stream)["project"]["version"]
    frontend_version = json.loads(
        (ROOT / "frontend/package.json").read_text(encoding="utf-8")
    )["version"]
    if backend_version != VERSION or frontend_version != VERSION:
        failures.append(
            f"version mismatch: backend={backend_version}, frontend={frontend_version}"
        )
    domain_source = ROOT / "frontend/src/types/domain.ts"
    if DISCLAIMER not in domain_source.read_text(encoding="utf-8"):
        failures.append(
            f"required disclaimer is absent from {domain_source.relative_to(ROOT)}"
        )
    if require_tags:
        tags = set(git_output("tag", "--points-at", "HEAD").splitlines())
        for tag in {"day-5-complete", "v1.0.0"} - tags:
            failures.append(f"release tag does not point at HEAD: {tag}")
    return failures


def main() -> int:
    """Run the default pre-tag release verification."""
    failures = collect_failures()
    if failures:
        print("PlayerPulse release verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PlayerPulse {VERSION} release verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
