"""Authorized fictional CSV import reaches persisted analytical APIs."""

import json
from pathlib import Path

from tests.api.test_datasets import api_client
from tests.api.test_upload_security import TRACKING_CSV


def test_local_tracking_import_reaches_dashboard_and_player_apis(
    tmp_path: Path,
) -> None:
    upload_manifest = json.dumps(
        {
            "source_match_id": "local-1",
            "competition": "Authorized fictional test",
            "rights_acknowledged": True,
            "files": [{"role": "tracking", "filename": "tracking.csv"}],
        }
    )
    with api_client(enable_uploads=True, data_root=tmp_path) as client:
        imported = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": upload_manifest,
            },
            files=[("files", ("tracking.csv", TRACKING_CSV, "text/csv"))],
        )
        assert imported.status_code == 201
        match_id = imported.json()["match_id"]

        match = client.get(f"/api/v1/matches/{match_id}")
        players = client.get(f"/api/v1/matches/{match_id}/players")
        quality = client.get(f"/api/v1/matches/{match_id}/quality")
        player_id = players.json()[0]["id"]
        metrics = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/metrics")
        timeline = client.get(
            f"/api/v1/matches/{match_id}/players/{player_id}/timeline"
        )
        heatmap = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/heatmap")
        events = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/events")
        risk = client.get(f"/api/v1/matches/{match_id}/players/{player_id}/risk")

    assert match.json()["is_synthetic"] is False
    assert match.json()["processing_status"] == "complete"
    assert len(players.json()) == 2
    assert quality.json()["data_quality_score"] == 1
    assert metrics.json()["total_distance_m"] > 0
    assert timeline.json()["point_count"] == 2
    assert heatmap.json()["rows"] == 8
    assert heatmap.json()["columns"] == 12
    assert events.json() == {"supported": False, "events": []}
    assert risk.status_code == 200
    assert risk.json()["assessment_status"] == "insufficient_data"
