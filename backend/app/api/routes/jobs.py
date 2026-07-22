"""Match processing and persisted job status endpoints."""

from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.models import Match
from app.db.session import get_session
from app.repositories.jobs import JobRepository
from app.services.processing import run_processing_job

router = APIRouter(prefix="/api/v1", tags=["processing"])


@router.post("/matches/{match_id}/process", status_code=202)
def process_match(
    match_id: UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, object]:
    """Queue an in-process task and persist its observable state."""
    if session.get(Match, match_id) is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    job = JobRepository(session).create(match_id)
    session.commit()
    settings = cast(Settings, request.app.state.settings)
    background_tasks.add_task(
        run_processing_job, session, job_id=job.id, seed=settings.synthetic_seed
    )
    return {"job_id": job.id, "status": job.status, "stage": job.stage}


@router.get("/jobs/{job_id}")
def job_status(
    job_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> dict[str, object]:
    """Return persisted job progress and safe failure information."""
    job = JobRepository(session).get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return {
        "id": job.id,
        "match_id": job.match_id,
        "status": job.status,
        "stage": job.stage,
        "progress": job.progress,
        "error_message": job.error_message,
        "started_at": job.started_at,
        "finished_at": job.finished_at,
        "limitation": "In-process jobs may need retry after a server restart.",
    }
