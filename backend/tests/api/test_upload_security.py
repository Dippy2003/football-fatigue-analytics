"""Multipart import contract and limits use fictional bytes only."""

import json
from pathlib import Path

import pytest

from tests.api.test_datasets import api_client

TRACKING_CSV = (
    b"match_id,period,frame_id,timestamp_seconds,team_id,player_id,"
    b"x,y,ball_x,ball_y\n"
    b"""\
local-1,1,0,0.0,Home,Home_1,0.1,0.2,0.5,0.5
local-1,1,1,1.0,Home,Home_1,0.11,0.2,0.5,0.5
local-1,1,0,0.0,Away,Away_1,0.9,0.8,0.5,0.5
local-1,1,1,1.0,Away,Away_1,0.89,0.8,0.5,0.5
"""
)


def manifest(filename: str = "tracking.csv", *, acknowledged: bool = True) -> str:
    return json.dumps(
        {
            "source_match_id": "local-1",
            "competition": "Authorized local test",
            "rights_acknowledged": acknowledged,
            "files": [{"role": "tracking", "filename": filename}],
        }
    )


def test_enabled_upload_processes_explicit_manifest(tmp_path: Path) -> None:
    with api_client(enable_uploads=True, data_root=tmp_path) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": manifest(),
            },
            files=[("files", ("tracking.csv", TRACKING_CSV, "text/csv"))],
        )
        repeated = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": manifest(),
            },
            files=[("files", ("tracking.csv", TRACKING_CSV, "text/csv"))],
        )

    assert response.status_code == 201
    assert response.json()["player_count"] == 2
    assert response.json()["quality_score"] == 100
    assert response.json()["is_synthetic"] is False
    assert response.json()["created"] is True
    assert repeated.status_code == 201
    assert repeated.json()["match_id"] == response.json()["match_id"]
    assert repeated.json()["player_count"] == 2
    assert repeated.json()["created"] is False


@pytest.mark.parametrize(
    ("upload_manifest", "filename", "expected_status"),
    [
        ("not-json", "tracking.csv", 422),
        ("{}", "tracking.csv", 422),
        (manifest("../tracking.csv"), "../tracking.csv", 415),
        (manifest("archive.zip"), "archive.zip", 415),
        (manifest("model.pkl"), "model.pkl", 415),
    ],
)
def test_invalid_upload_contract_is_rejected(
    upload_manifest: str,
    filename: str,
    expected_status: int,
) -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={"provider": "metrica_sample_data", "manifest": upload_manifest},
            files=[("files", (filename, b"fictional", "application/octet-stream"))],
        )

    assert response.status_code == expected_status


def test_upload_size_limit_is_enforced_before_parsing() -> None:
    oversized = b"x" * (1024 * 1024 + 1)
    with api_client(enable_uploads=True, max_upload_mb=1) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": manifest(),
            },
            files=[("files", ("tracking.csv", oversized, "text/csv"))],
        )

    assert response.status_code == 413


def test_upload_content_type_must_match_suffix() -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": manifest(),
            },
            files=[("files", ("tracking.csv", b"{}", "application/json"))],
        )

    assert response.status_code == 415
    assert response.json()["message"] == "File content type does not match its suffix."


def test_upload_requires_rights_acknowledgement() -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": manifest(acknowledged=False),
            },
            files=[("files", ("tracking.csv", TRACKING_CSV, "text/csv"))],
        )

    assert response.status_code == 422
    assert "rights" in response.json()["message"].lower()


def test_upload_rejects_unsupported_provider() -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={"provider": "statsbomb_open_data", "manifest": manifest()},
            files=[("files", ("tracking.csv", TRACKING_CSV, "text/csv"))],
        )

    assert response.status_code == 422
    assert "Metrica-compatible" in response.json()["message"]
