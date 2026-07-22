"""Dataset provenance and import-lineage persistence."""

from datetime import datetime

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now


class DatasetImport(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One immutable source-rights snapshot and its processing state."""

    __tablename__ = "dataset_imports"
    __table_args__ = (
        CheckConstraint(
            "import_status IN ('pending', 'processing', 'complete', 'failed')",
            name="import_status_allowed",
        ),
        Index("ix_dataset_imports_provider_status", "provider", "import_status"),
    )

    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    source_registry_id: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(500))
    rights_status_snapshot: Mapped[dict[str, object]] = mapped_column(
        JSON, nullable=False
    )
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    original_filename_manifest_json: Mapped[list[dict[str, object]]] = mapped_column(
        JSON, nullable=False, default=list
    )
    aggregate_checksum: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )
    import_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
