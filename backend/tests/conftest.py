"""Shared backend test fixtures and reliable temporary paths."""

from collections.abc import Iterator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pytest import Config

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Create an isolated synchronous API client."""
    with TestClient(create_app()) as test_client:
        yield test_client


def pytest_configure(config: Config) -> None:
    """Use a fresh workspace-local temp root when none was supplied."""
    if config.option.basetemp is None:
        config.option.basetemp = str(config.rootpath / f".pytest-run-{uuid4().hex}")
