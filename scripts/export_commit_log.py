"""Generate the documented PlayerPulse commit ledger from real Git history."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "COMMIT_LOG.md"
FIELD_SEPARATOR = "\x1f"


def git_output(*args: str) -> str:
    """Run a read-only Git command and return UTF-8 output."""
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def phase_for_commit(commit_hash: str, current_phase: str) -> str:
    """Derive the phase from existing checkpoint ancestry."""
    tags = set(git_output("tag", "--contains", commit_hash).splitlines())
    for day in range(1, 6):
        if f"day-{day}-complete" in tags:
            return f"Day {day}"
    return current_phase


def render(current_phase: str) -> str:
    """Render all commits through the current parent snapshot."""
    rows = git_output(
        "log",
        "--reverse",
        f"--format=%H{FIELD_SEPARATOR}%h{FIELD_SEPARATOR}%cI{FIELD_SEPARATOR}%s",
    ).splitlines()
    lines = [
        "# PlayerPulse commit log",
        "",
        "Generated from Git history by `scripts/export_commit_log.py`. "
        "Git remains the source of truth.",
        "",
        "| Phase | Commit | Timestamp | Purpose |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        full_hash, short_hash, timestamp, message = row.split(FIELD_SEPARATOR, 3)
        safe_message = message.replace("|", "\\|")
        phase = phase_for_commit(full_hash, current_phase)
        lines.append(f"| {phase} | `{short_hash}` | {timestamp} | {safe_message} |")
    lines.extend(
        [
            "",
            f"Commits recorded: **{len(rows)}**.",
            "",
            "The commit that updates this generated file cannot contain its own "
            "not-yet-known hash; the next checkpoint generation captures it.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    """Write the generated commit ledger."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--current-phase",
        default="Uncheckpointed",
        help="Label for commits not yet contained by a checkpoint tag.",
    )
    args = parser.parse_args()
    OUTPUT.write_text(render(args.current_phase), encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from current Git history.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
