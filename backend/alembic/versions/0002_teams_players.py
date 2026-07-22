"""Create teams and players.

Revision ID: 0002_teams_players
Revises: 0001_dataset_imports
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002_teams_players"
down_revision: str | None = "0001_dataset_imports"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create provider-scoped team and player identities."""
    op.create_table(
        "teams",
        sa.Column("external_id", sa.String(100), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("source", sa.String(80), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.UniqueConstraint(
            "source", "external_id", name="uq_teams_source_external_id"
        ),
    )
    op.create_table(
        "players",
        sa.Column("external_id", sa.String(100), nullable=False),
        sa.Column("team_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("position", sa.String(50), nullable=True),
        sa.Column("source", sa.String(80), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_players_team_id_teams"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        sa.UniqueConstraint(
            "source", "external_id", name="uq_players_source_external_id"
        ),
    )
    op.create_index(
        "ix_players_team_position", "players", ["team_id", "position"], unique=False
    )


def downgrade() -> None:
    """Drop players before teams."""
    op.drop_index("ix_players_team_position", table_name="players")
    op.drop_table("players")
    op.drop_table("teams")
