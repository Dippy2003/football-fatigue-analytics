"""Processing job model tests."""

from app.db.models import ProcessingJob


def test_processing_job_tracks_stage_progress_and_failures() -> None:
    columns = ProcessingJob.__table__.columns

    assert not columns["stage"].nullable
    assert not columns["progress"].nullable
    assert columns["error_message"].nullable
    assert columns["finished_at"].nullable
