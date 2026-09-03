"""Generate small, deterministic fictional CSVs for the local upload form."""

from pathlib import Path

from app.data.synthetic import generate_synthetic_events, generate_synthetic_tracking

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "frontend" / "public" / "samples"
MATCH_ID = "fictional-upload-003"


def main() -> int:
    """Write provider-shaped normalized tracking and event sample files."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tracking = generate_synthetic_tracking(
        seed=20_260_728,
        period_duration_s=60,
        sample_hz=10,
    )
    tracking["match_id"] = MATCH_ID
    tracking["x"] /= 105
    tracking["y"] /= 68
    tracking["ball_x"] /= 105
    tracking["ball_y"] /= 68
    tracking = tracking[
        [
            "match_id",
            "period",
            "frame_id",
            "timestamp_seconds",
            "team_id",
            "player_id",
            "x",
            "y",
            "ball_x",
            "ball_y",
            "source",
            "is_synthetic",
        ]
    ]
    tracking.to_csv(
        OUTPUT / "playerpulse-fictional-tracking.csv",
        index=False,
        lineterminator="\n",
        float_format="%.6f",
    )

    events = generate_synthetic_events(
        seed=20_260_728,
        period_duration_s=60,
    )
    events["match_id"] = MATCH_ID
    events["start_x"] /= 105
    events["start_y"] /= 68
    events["end_x"] /= 105
    events["end_y"] /= 68
    events = events[
        [
            "match_id",
            "event_id",
            "period",
            "timestamp_seconds",
            "team_id",
            "player_id",
            "event_type",
            "outcome",
            "start_x",
            "start_y",
            "end_x",
            "end_y",
            "source",
            "is_synthetic",
        ]
    ]
    events.to_csv(
        OUTPUT / "playerpulse-fictional-events.csv",
        index=False,
        lineterminator="\n",
        float_format="%.6f",
    )
    print(f"Wrote deterministic fictional upload samples to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
