"""FastAPI application for Endpoint Identity Control Plane."""

from datetime import UTC, datetime

from fastapi import FastAPI

from endpoint_identity_control_plane.demo_data import load_demo_inventory
from endpoint_identity_control_plane.models import Device, Group, User
from endpoint_identity_control_plane.risk import (
    Finding,
    RiskReport,
    build_risk_report,
    evaluate_inventory,
)

APP_NAME = "endpoint-identity-control-plane"
APP_VERSION = "0.1.0"
DATA_CLASSIFICATION = "synthetic-demo-data-only"
DEMO_REPORT_AS_OF = datetime(2026, 5, 22, 12, 0, tzinfo=UTC)

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


@app.get("/users")
def users() -> list[User]:
    """Return synthetic identity records."""
    return load_demo_inventory().users


@app.get("/devices")
def devices() -> list[Device]:
    """Return synthetic endpoint records."""
    return load_demo_inventory().devices


@app.get("/groups")
def groups() -> list[Group]:
    """Return synthetic identity group records."""
    return load_demo_inventory().groups


@app.get("/findings")
def findings() -> list[Finding]:
    """Return deterministic endpoint and identity findings for demo inventory."""
    inventory = load_demo_inventory()
    return evaluate_inventory(inventory, as_of=DEMO_REPORT_AS_OF)


@app.get("/risk-report")
def risk_report() -> RiskReport:
    """Return a summarized deterministic risk report for demo inventory."""
    inventory = load_demo_inventory()
    return build_risk_report(inventory, as_of=DEMO_REPORT_AS_OF)
