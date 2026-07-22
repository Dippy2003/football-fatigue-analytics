"""Dataset import lineage repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DatasetImport


class DatasetRepository:
    """Idempotent access to checksum-addressed dataset imports."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_checksum(self, checksum: str) -> DatasetImport | None:
        return self.session.scalar(
            select(DatasetImport).where(DatasetImport.aggregate_checksum == checksum)
        )

    def create_if_absent(
        self,
        *,
        provider: str,
        source_registry_id: str,
        checksum: str,
        rights_snapshot: dict[str, object],
        manifest: list[dict[str, object]],
        is_synthetic: bool,
    ) -> DatasetImport:
        existing = self.get_by_checksum(checksum)
        if existing is not None:
            return existing
        dataset_import = DatasetImport(
            provider=provider,
            source_registry_id=source_registry_id,
            source_url=None,
            rights_status_snapshot=rights_snapshot,
            is_synthetic=is_synthetic,
            original_filename_manifest_json=manifest,
            aggregate_checksum=checksum,
            import_status="pending",
        )
        self.session.add(dataset_import)
        self.session.flush()
        return dataset_import
