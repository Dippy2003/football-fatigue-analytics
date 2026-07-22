"""Dataset import repository tests."""

from app.core.config import Settings
from app.db.base import Base
from app.db.session import build_engine, build_session_factory
from app.repositories.datasets import DatasetRepository


def test_checksum_makes_dataset_creation_idempotent() -> None:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    with session_factory() as session:
        repository = DatasetRepository(session)
        arguments = {
            "provider": "PlayerPulse",
            "source_registry_id": "synthetic_playerpulse",
            "checksum": "a" * 64,
            "rights_snapshot": {"usage_status": "project_owned_synthetic"},
            "manifest": [],
            "is_synthetic": True,
        }
        first = repository.create_if_absent(**arguments)  # type: ignore[arg-type]
        second = repository.create_if_absent(**arguments)  # type: ignore[arg-type]

        assert first.id == second.id
        assert first.import_status == "pending"
    engine.dispose()
