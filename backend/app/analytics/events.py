"""Supported event workload and contribution metrics."""

from __future__ import annotations

import pandas as pd

DEFENSIVE_EVENTS = {"pressure", "tackle", "interception"}


def summarize_event_metrics(events: pd.DataFrame) -> pd.DataFrame:
    """Summarize supported events per player without inventing tracking context."""
    frame = events.copy()
    frame["is_pass"] = frame["event_type"].eq("pass")
    frame["is_completed_pass"] = frame["is_pass"] & frame["outcome"].eq("complete")
    frame["is_defensive_action"] = frame["event_type"].isin(DEFENSIVE_EVENTS)
    frame["is_possession_loss"] = frame["event_type"].eq("possession_loss")
    summary = (
        frame.groupby(["match_id", "team_id", "player_id"], dropna=False, sort=False)
        .agg(
            event_count=("event_id", "count"),
            pass_attempts=("is_pass", "sum"),
            completed_passes=("is_completed_pass", "sum"),
            defensive_actions=("is_defensive_action", "sum"),
            possession_losses=("is_possession_loss", "sum"),
        )
        .reset_index()
    )
    summary["pass_completion_rate"] = summary["completed_passes"].div(
        summary["pass_attempts"].where(summary["pass_attempts"] > 0)
    )
    return summary
