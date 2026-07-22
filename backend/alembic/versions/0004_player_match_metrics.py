"""Create player match metrics.

Revision ID: 0004_player_match_metrics
Revises: 0003_matches
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0004_player_match_metrics"
down_revision: str | None = "0003_matches"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create typed player-match feature summaries."""
    op.create_table(
        "player_match_metrics",
        sa.Column("match_id", sa.Uuid(), nullable=False),
        sa.Column("player_id", sa.Uuid(), nullable=False),
        sa.Column("playing_minutes", sa.Float(), nullable=False),
        sa.Column("total_distance_m", sa.Float(), nullable=False),
        sa.Column("distance_per_minute", sa.Float(), nullable=False),
        sa.Column("average_speed_mps", sa.Float(), nullable=False),
        sa.Column("max_speed_mps", sa.Float(), nullable=False),
        sa.Column("high_speed_distance_m", sa.Float(), nullable=False),
        sa.Column("sprint_count", sa.Integer(), nullable=False),
        sa.Column("sprint_distance_m", sa.Float(), nullable=False),
        sa.Column("median_sprint_recovery_seconds", sa.Float(), nullable=True),
        sa.Column("acceleration_count", sa.Integer(), nullable=False),
        sa.Column("deceleration_count", sa.Integer(), nullable=False),
        sa.Column("second_half_speed_change_pct", sa.Float(), nullable=True),
        sa.Column("late_match_sprint_change_pct", sa.Float(), nullable=True),
        sa.Column("late_match_distance_change_pct", sa.Float(), nullable=True),
        sa.Column("pass_accuracy_change_pct", sa.Float(), nullable=True),
        sa.Column("pressure_change_pct", sa.Float(), nullable=True),
        sa.Column("possession_loss_change", sa.Float(), nullable=True),
        sa.Column("workload_vs_baseline_zscore", sa.Float(), nullable=True),
        sa.Column("data_quality_score", sa.Float(), nullable=False),
        sa.Column("baseline_type", sa.String(50), nullable=True),
        sa.Column("baseline_confidence", sa.Float(), nullable=True),
        sa.Column("supported_event_metrics", sa.Boolean(), nullable=False),
        sa.Column("feature_version", sa.String(40), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
            name=op.f("fk_player_match_metrics_match_id_matches"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.id"],
            name=op.f("fk_player_match_metrics_player_id_players"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_player_match_metrics")),
        sa.UniqueConstraint("match_id", "player_id", name="uq_metrics_match_player"),
    )
    op.create_index(
        "ix_metrics_player_created",
        "player_match_metrics",
        ["player_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Drop player-match metrics."""
    op.drop_index("ix_metrics_player_created", table_name="player_match_metrics")
    op.drop_table("player_match_metrics")
