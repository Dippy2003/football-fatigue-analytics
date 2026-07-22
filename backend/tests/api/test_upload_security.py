"""Multipart upload contract and limit tests use fictional bytes only."""

import pytest

from tests.api.test_datasets import api_client


def test_enabled_upload_validates_explicit_manifest() -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={
                "provider": "metrica_sample_data",
                "manifest": '{"files": [{"role": "tracking"}]}',
            },
            files=[("files", ("tracking.csv", b"x,y\n0.5,0.5\n", "text/csv"))],
        )

    assert response.status_code == 202
    assert response.json() == {
        "status": "validated",
        "provider": "metrica_sample_data",
        "file_count": 1,
    }


@pytest.mark.parametrize(
    ("manifest", "filename", "expected_status"),
    [
        ("not-json", "tracking.csv", 422),
        ("{}", "tracking.csv", 422),
        ('{"files": []}', "../tracking.csv", 415),
        ('{"files": []}', "archive.zip", 415),
        ('{"files": []}', "model.pkl", 415),
    ],
)
def test_invalid_upload_contract_is_rejected(
    manifest: str, filename: str, expected_status: int
) -> None:
    with api_client(enable_uploads=True) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={"provider": "local", "manifest": manifest},
            files=[("files", (filename, b"fictional", "application/octet-stream"))],
        )

    assert response.status_code == expected_status


def test_upload_size_limit_is_enforced_before_parsing() -> None:
    oversized = b"x" * (1024 * 1024 + 1)
    with api_client(enable_uploads=True, max_upload_mb=1) as client:
        response = client.post(
            "/api/v1/datasets/upload",
            data={"provider": "local", "manifest": '{"files": []}'},
            files=[("files", ("tracking.csv", oversized, "text/csv"))],
        )

    assert response.status_code == 413
