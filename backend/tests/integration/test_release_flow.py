"""Complete synthetic processing-to-dashboard API contract."""

from tests.api.test_datasets import api_client


def test_synthetic_reviewer_flow_reaches_explainable_indicator() -> None:
    with api_client() as client:
        demo = client.post("/api/v1/datasets/demo").json()
        match_id = demo["match_id"]
        players = client.get(f"/api/v1/matches/{match_id}/players").json()
        player_id = players[0]["id"]

        match = client.get(f"/api/v1/matches/{match_id}")
        quality = client.get(f"/api/v1/matches/{match_id}/quality")
        metrics = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/metrics")
        timeline = client.get(
            f"/api/v1/matches/{match_id}/players/{player_id}/timeline"
        )
        heatmap = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/heatmap")
        risk = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/risk")
        baseline = client.get(f"/api/v1/players/{player_id}/baseline")

    assert demo["is_synthetic"] is True
    assert len(players) == 20
    assert match.status_code == quality.status_code == metrics.status_code == 200
    assert timeline.json()["point_count"] <= 121
    assert heatmap.json()["rows"] == 8
    assert heatmap.json()["columns"] == 12
    assert risk.json()["model_version"] == "rule-risk-v1"
    assert "not a medical diagnostic tool" in risk.json()["disclaimer"]
    assert baseline.json()["baseline_confidence"] == 0.4
