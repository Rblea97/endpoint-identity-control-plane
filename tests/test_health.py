from fastapi.testclient import TestClient

from endpoint_identity_control_plane.app import app


def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_returns_project_metadata() -> None:
    client = TestClient(app)
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "endpoint-identity-control-plane",
        "version": "0.1.0",
        "data_classification": "synthetic-demo-data-only",
    }
