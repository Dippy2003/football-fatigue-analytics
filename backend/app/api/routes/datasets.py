"""Dataset registry, synthetic demo, and guarded upload endpoints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, cast
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
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.data.registry import SourceRegistry
from app.db.session import get_session
from app.services.demo import create_demo_dataset

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])
ROOT = Path(__file__).parents[4]
ALLOWED_UPLOAD_SUFFIXES = {".csv", ".json"}


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


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_dataset(
    request: Request,
    provider: Annotated[str, Form()],
    manifest: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()],
) -> dict[str, object]:
    """Validate a bounded multipart contract; processing remains local-only."""
    settings = request_settings(request)
    if not settings.enable_uploads:
        raise HTTPException(status_code=403, detail="Third-party uploads are disabled.")
    if len(files) > settings.max_import_files:
        raise HTTPException(status_code=413, detail="Too many import files.")
    try:
        parsed_manifest = json.loads(manifest)
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=422, detail="Manifest must be valid JSON."
        ) from error
    if not isinstance(parsed_manifest, dict) or "files" not in parsed_manifest:
        raise HTTPException(status_code=422, detail="Manifest must declare file roles.")
    for upload in files:
        safe_name = Path(upload.filename or "").name
        if (
            safe_name != upload.filename
            or Path(safe_name).suffix.lower() not in ALLOWED_UPLOAD_SUFFIXES
        ):
            raise HTTPException(
                status_code=415, detail="Unsupported or unsafe filename."
            )
        if (
            upload.size is not None
            and upload.size > settings.max_upload_mb * 1024 * 1024
        ):
            raise HTTPException(
                status_code=413, detail="Import file exceeds size limit."
            )
        await upload.close()
    return {"status": "validated", "provider": provider, "file_count": len(files)}
