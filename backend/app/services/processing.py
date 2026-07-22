"""In-process match processing orchestration."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.data.processing import process_synthetic_demo
from app.db.models import Match
from app.repositories.jobs import JobRepository


def run_processing_job(session: Session, *, job_id: UUID, seed: int) -> None:
    """Run one synthetic match job and persist success or a bounded error."""
    jobs = JobRepository(session)
    job = jobs.get(job_id)
    if job is None:
        return
    match = session.get(Match, job.match_id)
    if match is None:
        jobs.finish(job, error="Match no longer exists.")
        session.commit()
        return
    try:
        jobs.mark_running(job, stage="canonical-data")
        jobs.update_progress(job, stage="analytics", progress=0.5)
        if match.is_synthetic:
            process_synthetic_demo(seed=seed)
        else:
            raise ValueError("External match reprocessing requires local source files.")
        match.processing_status = "complete"
        jobs.finish(job)
    except Exception:
        match.processing_status = "failed"
        jobs.finish(job, error="Processing failed; inspect safe server logs.")
    session.commit()
