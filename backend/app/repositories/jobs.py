"""Processing-job state transitions."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.base import utc_now
from app.db.models import ProcessingJob


class JobRepository:
    """Persist bounded, explicit in-process job transitions."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, match_id: UUID) -> ProcessingJob:
        job = ProcessingJob(match_id=match_id)
        self.session.add(job)
        self.session.flush()
        return job

    def get(self, job_id: UUID) -> ProcessingJob | None:
        return self.session.get(ProcessingJob, job_id)

    def mark_running(self, job: ProcessingJob, *, stage: str) -> None:
        job.status = "running"
        job.stage = stage
        job.started_at = job.started_at or utc_now()
        self.session.flush()

    def update_progress(
        self, job: ProcessingJob, *, stage: str, progress: float
    ) -> None:
        if not 0 <= progress <= 1:
            raise ValueError("job progress must be between 0 and 1")
        job.stage = stage
        job.progress = progress
        self.session.flush()

    def finish(self, job: ProcessingJob, *, error: str | None = None) -> None:
        job.status = "failed" if error else "complete"
        job.stage = "failed" if error else "complete"
        job.progress = job.progress if error else 1.0
        job.error_message = error
        job.finished_at = utc_now()
        self.session.flush()
