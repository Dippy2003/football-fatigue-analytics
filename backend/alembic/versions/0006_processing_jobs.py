"""Create processing jobs.

Revision ID: 0006_processing_jobs
Revises: 0005_risk_assessments
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0006_processing_jobs"
down_revision: str | None = "0005_risk_assessments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create persisted in-process job state."""
    op.create_table(
        "processing_jobs",
        sa.Column("match_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("stage", sa.String(80), nullable=False),
        sa.Column("progress", sa.Float(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'complete', 'failed')",
            name=op.f("ck_processing_jobs_status_allowed"),
        ),
        sa.CheckConstraint(
            "progress >= 0 AND progress <= 1",
            name=op.f("ck_processing_jobs_progress_bounds"),
        ),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
            name=op.f("fk_processing_jobs_match_id_matches"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_processing_jobs")),
    )
    op.create_index(
        "ix_jobs_status_created",
        "processing_jobs",
        ["status", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Drop processing jobs."""
    op.drop_index("ix_jobs_status_created", table_name="processing_jobs")
    op.drop_table("processing_jobs")
