"""Dataset registry, synthetic demo, and guarded upload endpoints."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field, ValidationError, model_validator
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.data.registry import SourceRegistry
from app.db.session import get_session
from app.services.demo import create_demo_dataset
from app.services.imports import import_metrica_match

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])
ROOT = Path(__file__).parents[4]
ALLOWED_UPLOAD_SUFFIXES = {".csv"}
ALLOWED_UPLOAD_TYPES = {
    ".csv": {"text/csv", "application/csv", "application/vnd.ms-excel"},
}


class DemoDatasetResponse(BaseModel):
    """Idempotent synthetic demo creation result."""

    dataset_import_id: UUID
    match_id: UUID
    player_count: int
    is_synthetic: bool
    created: bool


class SourceResponse(BaseModel):
    """Safe public source-registry summary."""

    id: str
    provider: str
    usage_status: str
    attribution: str


class UploadFileDeclaration(BaseModel):
    """Declared role for one multipart file."""

    role: Literal["tracking", "events"]
    filename: str = Field(min_length=1, max_length=255)


class LocalUploadManifest(BaseModel):
    """Rights acknowledgement and match metadata for a local import."""

    source_match_id: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9._-]+$",
    )
    competition: str = Field(default="Local authorized import", max_length=160)
    rights_acknowledged: bool
    files: list[UploadFileDeclaration] = Field(min_length=1, max_length=2)

    @model_validator(mode="after")
    def validate_roles(self) -> LocalUploadManifest:
        roles = [item.role for item in self.files]
        filenames = [item.filename for item in self.files]
        if roles.count("tracking") != 1:
            raise ValueError("Manifest must declare exactly one tracking file.")
        if len(roles) != len(set(roles)) or len(filenames) != len(set(filenames)):
            raise ValueError("Manifest file roles and filenames must be unique.")
        return self


class ImportCapabilitiesResponse(BaseModel):
    """Safe description of the locally enabled import workflow."""

    uploads_enabled: bool
    provider: Literal["metrica_sample_data"] = "metrica_sample_data"
    tracking_required: bool = True
    events_optional: bool = True
    accepted_extensions: list[str] = [".csv"]
    max_upload_mb: int
    max_import_rows: int


class LocalImportResponse(BaseModel):
    """Created dashboard identity and quality summary."""

    dataset_import_id: UUID
    match_id: UUID
    player_count: int
    quality_score: float
    quality_confidence: str
    limitations: list[str]
    is_synthetic: bool = False
    created: bool


def request_settings(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


@router.post(
    "/demo", response_model=DemoDatasetResponse, status_code=status.HTTP_201_CREATED
)
def create_demo(
    session: Annotated[Session, Depends(get_session)], request: Request
) -> DemoDatasetResponse:
    """Create or return the deterministic fictional demonstration dataset."""
    result = create_demo_dataset(session, seed=request_settings(request).synthetic_seed)
    return DemoDatasetResponse(
        dataset_import_id=result.dataset_import.id,
        match_id=result.match.id,
        player_count=len(result.players),
        is_synthetic=True,
        created=result.created,
    )


@router.get("/sources", response_model=list[SourceResponse])
def list_sources() -> list[SourceResponse]:
    """Return rights status and attribution without importing source files."""
    registry = SourceRegistry.load(ROOT / "data" / "sources.yml")
    return [
        SourceResponse(
            id=source.id,
            provider=source.provider,
            usage_status=source.usage_status.value,
            attribution=source.attribution,
        )
        for source in registry.sources
    ]


@router.get("/import-capabilities", response_model=ImportCapabilitiesResponse)
def import_capabilities(request: Request) -> ImportCapabilitiesResponse:
    """Tell the UI whether guarded local imports are enabled."""
    settings = request_settings(request)
    return ImportCapabilitiesResponse(
        uploads_enabled=settings.enable_uploads,
        max_upload_mb=settings.max_upload_mb,
        max_import_rows=settings.max_import_rows,
    )


@router.post(
    "/upload",
    response_model=LocalImportResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_dataset(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    provider: Annotated[str, Form()],
    manifest: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()],
) -> LocalImportResponse:
    """Process an authorized local tracking CSV into dashboard-ready summaries."""
    settings = request_settings(request)
    if not settings.enable_uploads:
        raise HTTPException(status_code=403, detail="Third-party uploads are disabled.")
    if provider != "metrica_sample_data":
        raise HTTPException(
            status_code=422,
            detail="Only Metrica-compatible long-form tracking imports are supported.",
        )
    if len(files) > settings.max_import_files:
        raise HTTPException(status_code=413, detail="Too many import files.")
    try:
        parsed_manifest = LocalUploadManifest.model_validate_json(manifest)
    except (json.JSONDecodeError, ValidationError) as error:
        raise HTTPException(
            status_code=422,
            detail="Manifest is invalid or missing required import metadata.",
        ) from error
    if not parsed_manifest.rights_acknowledged:
        raise HTTPException(
            status_code=422,
            detail="Current source rights must be acknowledged before import.",
        )
    registry = SourceRegistry.load(ROOT / "data" / "sources.yml")
    source = registry.get(provider)
    if not source.allows_import(supplied_locally=True):
        raise HTTPException(
            status_code=403,
            detail="The source registry does not permit this local import.",
        )
    declared_by_filename = {
        declaration.filename: declaration.role for declaration in parsed_manifest.files
    }
    if {upload.filename for upload in files} != set(declared_by_filename):
        raise HTTPException(
            status_code=422,
            detail="Multipart files must exactly match the manifest declarations.",
        )
    file_bytes: dict[str, bytes] = {}
    original_manifest: list[dict[str, object]] = []
    for upload in files:
        safe_name = Path(upload.filename or "").name
        suffix = Path(safe_name).suffix.lower()
        if safe_name != upload.filename or suffix not in ALLOWED_UPLOAD_SUFFIXES:
            raise HTTPException(
                status_code=415, detail="Unsupported or unsafe filename."
            )
        if upload.content_type not in ALLOWED_UPLOAD_TYPES[suffix]:
            raise HTTPException(
                status_code=415, detail="File content type does not match its suffix."
            )
        if (
            upload.size is not None
            and upload.size > settings.max_upload_mb * 1024 * 1024
        ):
            raise HTTPException(
                status_code=413, detail="Import file exceeds size limit."
            )
        total = 0
        chunks: list[bytes] = []
        while chunk := await upload.read(64 * 1024):
            total += len(chunk)
            if total > settings.max_upload_mb * 1024 * 1024:
                await upload.close()
                raise HTTPException(
                    status_code=413, detail="Import file exceeds size limit."
                )
            chunks.append(chunk)
        await upload.close()
        file_bytes[safe_name] = b"".join(chunks)
        original_manifest.append(
            {
                "role": declared_by_filename[safe_name],
                "original_name": safe_name,
                "size_bytes": total,
                "sha256": hashlib.sha256(file_bytes[safe_name]).hexdigest(),
            }
        )
    with TemporaryDirectory(prefix="playerpulse-import-") as temporary:
        temporary_path = Path(temporary)
        role_paths: dict[str, Path] = {}
        role_bytes: dict[str, bytes] = {}
        for filename, content in file_bytes.items():
            role = declared_by_filename[filename]
            path = temporary_path / filename
            path.write_bytes(content)
            role_paths[role] = path
            role_bytes[role] = content
        try:
            result = import_metrica_match(
                session,
                source=source,
                source_match_id=parsed_manifest.source_match_id,
                competition=parsed_manifest.competition,
                tracking_path=role_paths["tracking"],
                tracking_bytes=role_bytes["tracking"],
                events_path=role_paths.get("events"),
                events_bytes=role_bytes.get("events"),
                original_manifest=original_manifest,
                data_root=settings.data_root,
                max_rows=settings.max_import_rows,
            )
        except (KeyError, PermissionError, UnicodeDecodeError, ValueError) as error:
            session.rollback()
            raise HTTPException(
                status_code=422,
                detail=f"Import could not be processed: {error}",
            ) from error
    return LocalImportResponse(
        dataset_import_id=result.dataset_import.id,
        match_id=result.match.id,
        player_count=len(result.players),
        quality_score=result.processing.quality.quality_score,
        quality_confidence=result.processing.quality.confidence,
        limitations=result.processing.quality.limitations,
        created=result.created,
    )
