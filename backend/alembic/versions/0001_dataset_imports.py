"""Create dataset import lineage.

Revision ID: 0001_dataset_imports
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_dataset_imports"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the dataset import lineage table."""
    op.create_table(
        "dataset_imports",
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("source_registry_id", sa.String(length=100), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("rights_status_snapshot", sa.JSON(), nullable=False),
        sa.Column("is_synthetic", sa.Boolean(), nullable=False),
        sa.Column("original_filename_manifest_json", sa.JSON(), nullable=False),
        sa.Column("aggregate_checksum", sa.String(length=64), nullable=False),
        sa.Column("import_status", sa.String(length=20), nullable=False),
        sa.Column("imported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "import_status IN ('pending', 'processing', 'complete', 'failed')",
            name=op.f("ck_dataset_imports_import_status_allowed"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_imports")),
        sa.UniqueConstraint(
            "aggregate_checksum", name=op.f("uq_dataset_imports_aggregate_checksum")
        ),
    )
    op.create_index(
        "ix_dataset_imports_provider_status",
        "dataset_imports",
        ["provider", "import_status"],
        unique=False,
    )


def downgrade() -> None:
    """Drop dataset import lineage."""
    op.drop_index("ix_dataset_imports_provider_status", table_name="dataset_imports")
    op.drop_table("dataset_imports")
