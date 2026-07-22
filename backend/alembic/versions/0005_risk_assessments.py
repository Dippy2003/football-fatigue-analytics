"""Create risk assessments.

Revision ID: 0005_risk_assessments
Revises: 0004_player_match_metrics
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005_risk_assessments"
down_revision: str | None = "0004_player_match_metrics"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create versioned explainable risk assessments."""
    op.create_table(
        "risk_assessments",
        sa.Column("match_id", sa.Uuid(), nullable=False),
        sa.Column("player_id", sa.Uuid(), nullable=False),
        sa.Column("assessment_status", sa.String(30), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("category", sa.String(60), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("rule_score", sa.Float(), nullable=True),
        sa.Column("anomaly_score", sa.Float(), nullable=True),
        sa.Column("explanation_json", sa.JSON(), nullable=False),
        sa.Column("model_version", sa.String(60), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "assessment_status IN ('available', 'insufficient_data')",
            name=op.f("ck_risk_assessments_assessment_status_allowed"),
        ),
        sa.CheckConstraint(
            "score IS NULL OR (score >= 0 AND score <= 100)",
            name=op.f("ck_risk_assessments_score_bounds"),
        ),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
            name=op.f("fk_risk_assessments_match_id_matches"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.id"],
            name=op.f("fk_risk_assessments_player_id_players"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_risk_assessments")),
    )
    op.create_index(
        "ix_risk_match_player_created",
        "risk_assessments",
        ["match_id", "player_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Drop risk assessments."""
    op.drop_index("ix_risk_match_player_created", table_name="risk_assessments")
    op.drop_table("risk_assessments")
