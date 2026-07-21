"""Immutable provenance metadata for local import files."""

from __future__ import annotations

import hashlib
import mimetypes
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from app.data.importers.common import require_local_file
from app.data.registry import SourceRecord


class ImportFileRecord(BaseModel):
    """Checksum-backed record of a single imported file."""

    model_config = ConfigDict(extra="forbid")

    file_role: str
    original_name: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)
    mime_type: str


class ImportManifest(BaseModel):
    """Source, rights snapshot, and files for one local import."""

    model_config = ConfigDict(extra="forbid")

    source_id: str
    source_match_id: str
    is_synthetic: bool
    imported_at_utc: datetime
    rights_snapshot: dict[str, object]
    files: list[ImportFileRecord]


def fingerprint_file(path: Path, *, role: str) -> ImportFileRecord:
    """Stream a file into a SHA-256 provenance record."""
    resolved = require_local_file(path)
    digest = hashlib.sha256()
    with resolved.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    mime_type = mimetypes.guess_type(resolved.name)[0] or "application/octet-stream"
    return ImportFileRecord(
        file_role=role,
        original_name=resolved.name,
        sha256=digest.hexdigest(),
        size_bytes=resolved.stat().st_size,
        mime_type=mime_type,
    )


def build_import_manifest(
    *,
    source: SourceRecord,
    source_match_id: str,
    files: list[tuple[str, Path]],
    imported_at_utc: datetime | None = None,
) -> ImportManifest:
    """Build a manifest without copying or redistributing source data."""
    timestamp = imported_at_utc or datetime.now(UTC)
    return ImportManifest(
        source_id=source.id,
        source_match_id=source_match_id,
        is_synthetic=source.usage_status.value == "project_owned_synthetic",
        imported_at_utc=timestamp,
        rights_snapshot=source.model_dump(mode="json"),
        files=[fingerprint_file(path, role=role) for role, path in files],
    )
