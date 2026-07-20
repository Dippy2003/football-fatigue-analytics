"""Tests for operational API routes."""

from fastapi.testclient import TestClient


def test_health_reports_process_liveness(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_current_checks(client: TestClient) -> None:
    response = client.get("/api/v1/readiness")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"application": "ok"},
    }


def test_version_exposes_public_build_identity(client: TestClient) -> None:
    response = client.get("/api/v1/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PlayerPulse API",
        "version": "0.1.0",
        "api_version": "v1",
    }


def test_openapi_uses_versioned_schema_path(client: TestClient) -> None:
    response = client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    assert "/api/v1/health" in response.json()["paths"]
