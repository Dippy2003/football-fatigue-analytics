"""Standard API error-contract tests."""

from tests.api.test_datasets import api_client


def test_not_found_error_includes_request_id_and_timestamp() -> None:
    with api_client() as client:
        response = client.get(
            "/api/v1/matches/00000000-0000-0000-0000-000000000000",
            headers={"X-Request-ID": "portfolio-check-1"},
        )

    payload = response.json()
    assert response.status_code == 404
    assert payload["code"] == "http_404"
    assert payload["message"] == "Match not found."
    assert payload["request_id"] == "portfolio-check-1"
    assert "timestamp" in payload
    assert response.headers["X-Request-ID"] == "portfolio-check-1"


def test_validation_errors_use_same_contract() -> None:
    with api_client() as client:
        response = client.get("/api/v1/players/not-a-uuid")

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
    assert isinstance(response.json()["details"], list)
