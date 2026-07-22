"""Create matches.

Revision ID: 0003_matches
Revises: 0002_teams_players
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003_matches"
down_revision: str | None = "0002_teams_players"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create matches with lineage and provider identity."""
    op.create_table(
        "matches",
        sa.Column("external_id", sa.String(100), nullable=False),
        sa.Column("home_team_id", sa.Uuid(), nullable=False),
        sa.Column("away_team_id", sa.Uuid(), nullable=False),
        sa.Column("competition", sa.String(160), nullable=True),
        sa.Column("match_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("pitch_length_m", sa.Float(), nullable=False),
        sa.Column("pitch_width_m", sa.Float(), nullable=False),
        sa.Column("source", sa.String(80), nullable=False),
        sa.Column("dataset_import_id", sa.Uuid(), nullable=False),
        sa.Column("is_synthetic", sa.Boolean(), nullable=False),
        sa.Column("processing_status", sa.String(20), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "home_team_id <> away_team_id", name=op.f("ck_matches_different_teams")
        ),
        sa.CheckConstraint(
            "processing_status IN ('pending', 'processing', 'complete', 'failed')",
            name=op.f("ck_matches_processing_status_allowed"),
        ),
        sa.ForeignKeyConstraint(
            ["away_team_id"],
            ["teams.id"],
            name=op.f("fk_matches_away_team_id_teams"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["dataset_import_id"],
            ["dataset_imports.id"],
            name=op.f("fk_matches_dataset_import_id_dataset_imports"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["home_team_id"],
            ["teams.id"],
            name=op.f("fk_matches_home_team_id_teams"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches")),
        sa.UniqueConstraint(
            "source", "external_id", name="uq_matches_source_external_id"
        ),
    )
    op.create_index(
        "ix_matches_date_status",
        "matches",
        ["match_date", "processing_status"],
        unique=False,
    )


def downgrade() -> None:
    """Drop matches."""
    op.drop_index("ix_matches_date_status", table_name="matches")
    op.drop_table("matches")
