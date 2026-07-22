"""Processing job transition tests."""

from uuid import uuid4

import pytest

from app.core.config import Settings
from app.db.base import Base
from app.db.session import build_engine, build_session_factory
from app.repositories.jobs import JobRepository


def test_job_repository_tracks_successful_transition() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        repository = JobRepository(session)
        job = repository.create(uuid4())
        repository.mark_running(job, stage="features")
        repository.update_progress(job, stage="risk", progress=0.8)
        repository.finish(job)

        assert job.status == "complete"
        assert job.progress == 1
        assert job.started_at is not None
        assert job.finished_at is not None
    engine.dispose()


def test_job_repository_rejects_invalid_progress() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        repository = JobRepository(session)
        job = repository.create(uuid4())
        with pytest.raises(ValueError, match="between 0 and 1"):
            repository.update_progress(job, stage="invalid", progress=1.1)
    engine.dispose()
