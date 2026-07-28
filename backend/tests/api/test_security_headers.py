"""Security response headers protect every public API response."""

from fastapi.testclient import TestClient


def test_api_responses_include_browser_safeguards(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"
    assert "camera=()" in response.headers["permissions-policy"]
