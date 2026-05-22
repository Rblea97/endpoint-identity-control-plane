"""FastAPI application for Endpoint Identity Control Plane."""

from fastapi import FastAPI

APP_NAME = "endpoint-identity-control-plane"
APP_VERSION = "0.1.0"
DATA_CLASSIFICATION = "synthetic-demo-data-only"

app = FastAPI(
    title="Endpoint Identity Control Plane",
    summary="Endpoint and identity risk-scoring lab using synthetic data.",
    version=APP_VERSION,
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal health response for local and CI smoke checks."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    """Return project metadata for smoke tests and demo documentation."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "data_classification": DATA_CLASSIFICATION,
    }
