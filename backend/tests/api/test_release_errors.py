"""Release API rejects malformed identifiers and comparison bounds."""

from fastapi.testclient import TestClient


def test_malformed_uuid_returns_safe_validation_error(client: TestClient) -> None:
    response = client.get("/api/v1/matches/not-a-uuid")

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
    assert "traceback" not in response.text.lower()


def test_comparison_requires_two_to_four_players(client: TestClient) -> None:
    response = client.get(
        "/api/v1/matches/00000000-0000-0000-0000-000000000001/compare-players",
        params={"player_ids": "00000000-0000-0000-0000-000000000002"},
    )

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
