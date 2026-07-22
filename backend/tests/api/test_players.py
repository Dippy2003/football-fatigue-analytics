"""Player analytics endpoint tests."""

from tests.api.test_datasets import api_client


def test_player_endpoints_return_bounded_synthetic_results() -> None:
    with api_client() as client:
        match_id = client.post("/api/v1/datasets/demo").json()["match_id"]
        player = client.get(f"/api/v1/matches/{match_id}/players").json()[0]
        player_id = player["id"]

        profile = client.get(f"/api/v1/players/{player_id}")
        history = client.get(f"/api/v1/players/{player_id}/matches")
        metrics = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/metrics")
        timeline = client.get(
            f"/api/v1/matches/{match_id}/players/{player_id}/timeline"
        )
        heatmap = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/heatmap")
        events = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/events")
        baseline = client.get(f"/api/v1/players/{player_id}/baseline")

    assert profile.status_code == 200
    assert len(history.json()) == 1
    assert metrics.json()["feature_version"] == "features-v1"
    assert timeline.json()["point_count"] <= 121
    assert len(heatmap.json()["grid"]) == 8
    assert len(heatmap.json()["grid"][0]) == 12
    assert events.json()["supported"] is True
    assert baseline.json()["baseline_type"] == "match_only"
