"""Risk and comparison endpoint tests."""

from tests.api.test_datasets import api_client


def test_risk_response_is_explainable_and_non_medical() -> None:
    with api_client() as client:
        match_id = client.post("/api/v1/datasets/demo").json()["match_id"]
        player = client.get(f"/api/v1/matches/{match_id}/players").json()[0]
        response = client.get(f"/api/v1/matches/{match_id}/players/{player['id']}/risk")

    payload = response.json()
    assert response.status_code == 200
    assert payload["assessment_status"] in {"available", "insufficient_data"}
    assert payload["model_version"] == "rule-risk-v1"
    assert "not a medical diagnostic tool" in payload["disclaimer"]
    assert "confidence" in payload
    assert "limitations" in payload


def test_player_comparison_returns_aligned_metrics() -> None:
    with api_client() as client:
        match_id = client.post("/api/v1/datasets/demo").json()["match_id"]
        players = client.get(f"/api/v1/matches/{match_id}/players").json()[:2]
        response = client.get(
            f"/api/v1/matches/{match_id}/compare-players",
            params=[("player_ids", player["id"]) for player in players],
        )

    assert response.status_code == 200
    assert len(response.json()["players"]) == 2
    assert "context" in response.json()["warning"]
