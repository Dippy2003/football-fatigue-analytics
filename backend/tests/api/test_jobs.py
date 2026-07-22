"""Processing job API tests."""

from tests.api.test_datasets import api_client


def test_match_processing_exposes_persisted_job_status() -> None:
    with api_client() as client:
        match_id = client.post("/api/v1/datasets/demo").json()["match_id"]
        queued = client.post(f"/api/v1/matches/{match_id}/process")
        status = client.get(f"/api/v1/jobs/{queued.json()['job_id']}")

    assert queued.status_code == 202
    assert status.status_code == 200
    assert status.json()["status"] == "complete"
    assert status.json()["progress"] == 1
    assert "server restart" in status.json()["limitation"]
