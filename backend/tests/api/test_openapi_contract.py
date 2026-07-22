"""Published OpenAPI surface tests."""

from tests.api.test_datasets import api_client


def test_openapi_and_swagger_publish_implemented_routes() -> None:
    with api_client() as client:
        schema_response = client.get("/api/v1/openapi.json")
        docs_response = client.get("/docs")

    paths = schema_response.json()["paths"]
    assert schema_response.status_code == 200
    assert docs_response.status_code == 200
    assert "/api/v1/datasets/demo" in paths
    assert "/api/v1/matches/{match_id}/players/{player_id}/risk" in paths
    assert "/api/v1/matches/{match_id}/players/{player_id}/heatmap" in paths
    assert "/api/v1/jobs/{job_id}" in paths
