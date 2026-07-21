"""Developer commands for deterministic local data processing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.data.processing import process_synthetic_demo


def build_parser() -> argparse.ArgumentParser:
    """Build the stable command-line interface."""
    parser = argparse.ArgumentParser(prog="playerpulse-data")
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser(
        "generate-demo", help="generate deterministic fictional Parquet tables"
    )
    demo.add_argument("--output", type=Path, required=True)
    demo.add_argument("--seed", type=int, default=20250714)
    demo.add_argument("--period-duration", type=int, default=180)
    return parser


def main(arguments: list[str] | None = None) -> int:
    """Run a data command and print a machine-readable result summary."""
    args = build_parser().parse_args(arguments)
    if args.command == "generate-demo":
        result = process_synthetic_demo(
            output_directory=args.output,
            seed=args.seed,
            period_duration_s=args.period_duration,
        )
        print(
            json.dumps(
                {
                    "is_synthetic": True,
                    "quality": result.quality.model_dump(),
                    "outputs": {
                        name: str(path) for name, path in result.output_paths.items()
                    },
                },
                indent=2,
            )
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
