"""Dataset API tests with synthetic data only."""

from collections.abc import Iterator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.base import Base
from app.db.session import build_engine, build_session_factory, get_session
from app.main import create_app


@contextmanager
def api_client(*, enable_uploads: bool = False) -> Iterator[TestClient]:
    engine = build_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    app = create_app(
        Settings(
            database_url="sqlite+pysqlite:///:memory:",
            enable_uploads=enable_uploads,
            synthetic_seed=42,
        )
    )

    def session_override() -> Iterator[Session]:
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    with TestClient(app) as client:
        yield client
    engine.dispose()


def test_sources_returns_rights_status_and_attribution() -> None:
    with api_client() as client:
        response = client.get("/api/v1/datasets/sources")

    assert response.status_code == 200
    assert {source["id"] for source in response.json()} == {
        "synthetic_playerpulse",
        "metrica_sample_data",
        "statsbomb_open_data",
    }


def test_demo_endpoint_persists_idempotent_match() -> None:
    with api_client() as client:
        first = client.post("/api/v1/datasets/demo")
        second = client.post("/api/v1/datasets/demo")

    assert first.status_code == 201
    assert first.json()["is_synthetic"] is True
    assert first.json()["player_count"] == 20
    assert first.json()["created"] is True
    assert second.json()["created"] is False
    assert first.json()["match_id"] == second.json()["match_id"]


def test_upload_endpoint_fails_closed_by_default() -> None:
    with api_client() as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={"provider": "metrica", "manifest": '{"files": []}'},
            files=[("files", ("tracking.csv", b"x,y\n", "text/csv"))],
        )

    assert response.status_code == 403
    assert response.json()["message"] == "Third-party uploads are disabled."
    assert response.json()["code"] == "http_403"
