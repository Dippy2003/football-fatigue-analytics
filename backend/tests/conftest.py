"""Shared backend test fixtures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Create an isolated synchronous API client."""
    with TestClient(create_app()) as test_client:
        yield test_client

