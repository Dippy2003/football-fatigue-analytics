"""Stored match endpoint tests."""

from fastapi.testclient import TestClient

from tests.api.test_datasets import api_client


def create_demo(client: TestClient) -> str:
    return str(client.post("/api/v1/datasets/demo").json()["match_id"])


def test_match_endpoints_return_stored_demo_summaries() -> None:
    with api_client() as client:
        match_id = create_demo(client)

        matches = client.get("/api/v1/matches")
        detail = client.get(f"/api/v1/matches/{match_id}")
        players = client.get(f"/api/v1/matches/{match_id}/players")
        teams = client.get(f"/api/v1/matches/{match_id}/team-summary")
        quality = client.get(f"/api/v1/matches/{match_id}/quality")

    assert len(matches.json()) == 1
    assert detail.json()["is_synthetic"] is True
    assert len(players.json()) == 20
    assert len(teams.json()) == 2
    assert quality.json()["data_quality_score"] == 1
    assert quality.json()["player_metric_coverage"] == 20


def test_unknown_match_returns_not_found() -> None:
    with api_client() as client:
        response = client.get("/api/v1/matches/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
