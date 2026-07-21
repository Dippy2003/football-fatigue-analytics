"""Deterministic fictional match data for demos, tests, and CI."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticMatch:
    """Canonical synthetic tracking and event tables."""

    tracking: pd.DataFrame
    events: pd.DataFrame


def _player_ids() -> list[tuple[str, str]]:
    return [
        (team, f"{team}-{number:02d}")
        for team in ("home", "away")
        for number in range(1, 10)
    ]


def generate_synthetic_tracking(
    *, seed: int = 20250714, period_duration_s: int = 180, sample_hz: int = 10
) -> pd.DataFrame:
    """Build repeatable two-period tracking for 18 fictional players."""
    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []
    players = _player_ids()
    for period in (1, 2):
        for sample in range(period_duration_s * sample_hz + 1):
            second = sample / sample_hz
            absolute = (period - 1) * period_duration_s + second
            ball_x = 52.5 + 32 * np.sin(absolute / 23)
            ball_y = 34 + 20 * np.cos(absolute / 17)
            for index, (team, player_id) in enumerate(players):
                shirt = (index % 9) + 1
                phase = shirt * 0.61 + (0 if team == "home" else np.pi)
                direction = 1 if team == "home" else -1
                workload = 1.0 if shirt <= 6 else 1.18
                decline = 1 - (0.0007 * absolute if shirt in (3, 8) else 0)
                x = 52.5 + direction * 18 + 20 * np.sin(absolute / 12 + phase)
                y = 34 + 25 * np.cos(absolute / 15 + phase)
                x += workload * decline * np.sin(absolute / 2.7 + phase)
                y += workload * decline * np.cos(absolute / 3.1 + phase)
                rows.append(
                    {
                        "match_id": "synthetic-match-001",
                        "period": period,
                        "frame_id": (period - 1) * period_duration_s * sample_hz
                        + sample,
                        "timestamp_seconds": float(second),
                        "team_id": team,
                        "player_id": player_id,
                        "x": float(np.clip(x + rng.normal(0, 0.03), 0, 105)),
                        "y": float(np.clip(y + rng.normal(0, 0.03), 0, 68)),
                        "ball_x": float(np.clip(ball_x, 0, 105)),
                        "ball_y": float(np.clip(ball_y, 0, 68)),
                        "source": "synthetic_playerpulse",
                        "is_synthetic": True,
                    }
                )
    frame = pd.DataFrame(rows)
    # A short deterministic dropout exercises cleaning without corrupting the demo.
    dropout = (
        (frame["player_id"] == "home-06")
        & (frame["period"] == 2)
        & frame["timestamp_seconds"].between(80.1, 80.2)
    )
    frame.loc[dropout, ["x", "y"]] = np.nan
    return frame


def generate_synthetic_events(
    *, seed: int = 20250714, period_duration_s: int = 180
) -> pd.DataFrame:
    """Build repeatable canonical events covering supported event families."""
    rng = np.random.default_rng(seed + 1)
    event_types = ("pass", "pressure", "tackle", "interception", "possession_loss")
    rows: list[dict[str, object]] = []
    event_id = 0
    for period in (1, 2):
        for second in range(5, period_duration_s, 5):
            team = "home" if (second // 5 + period) % 2 == 0 else "away"
            event_type = event_types[event_id % len(event_types)]
            start_x = float(rng.uniform(5, 100))
            start_y = float(rng.uniform(3, 65))
            is_pass = event_type == "pass"
            rows.append(
                {
                    "match_id": "synthetic-match-001",
                    "event_id": f"synthetic-event-{event_id:04d}",
                    "period": period,
                    "timestamp_seconds": float(second),
                    "team_id": team,
                    "player_id": f"{team}-{(event_id % 9) + 1:02d}",
                    "event_type": event_type,
                    "outcome": "complete" if is_pass else "observed",
                    "start_x": start_x,
                    "start_y": start_y,
                    "end_x": float(np.clip(start_x + rng.normal(8, 5), 0, 105))
                    if is_pass
                    else np.nan,
                    "end_y": float(np.clip(start_y + rng.normal(0, 5), 0, 68))
                    if is_pass
                    else np.nan,
                    "source": "synthetic_playerpulse",
                    "is_synthetic": True,
                }
            )
            event_id += 1
    return pd.DataFrame(rows)


def generate_synthetic_match(
    *, seed: int = 20250714, period_duration_s: int = 180
) -> SyntheticMatch:
    """Return the only dataset enabled by default for public demonstrations."""
    return SyntheticMatch(
        tracking=generate_synthetic_tracking(
            seed=seed, period_duration_s=period_duration_s
        ),
        events=generate_synthetic_events(
            seed=seed, period_duration_s=period_duration_s
        ),
    )
