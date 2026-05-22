from fastapi.testclient import TestClient

from endpoint_identity_control_plane.app import app


def test_users_endpoint_returns_synthetic_users() -> None:
    client = TestClient(app)
    response = client.get("/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 3
    assert all(user["username"].endswith(".example") for user in users)
    assert {"id", "username", "mfa_enabled", "assigned_device_ids"} <= set(users[0])


def test_devices_endpoint_returns_synthetic_devices() -> None:
    client = TestClient(app)
    response = client.get("/devices")

    assert response.status_code == 200
    devices = response.json()
    assert len(devices) >= 3
    assert all(device["hostname"].startswith("DEMO-") for device in devices)
    assert {"id", "hostname", "patch_status", "compliance_state"} <= set(devices[0])


def test_groups_endpoint_returns_synthetic_groups() -> None:
    client = TestClient(app)
    response = client.get("/groups")

    assert response.status_code == 200
    groups = response.json()
    assert len(groups) >= 2
    assert {"id", "name", "privilege_level", "member_user_ids"} <= set(groups[0])


def test_findings_endpoint_returns_prioritized_findings() -> None:
    client = TestClient(app)
    response = client.get("/findings")

    assert response.status_code == 200
    findings = response.json()
    finding_ids = {finding["id"] for finding in findings}
    assert "identity-privileged-user-missing-mfa-user-002" in finding_ids
    assert "endpoint-encryption-disabled-device-003" in finding_ids
    assert all(finding["recommendation"] for finding in findings)
    assert all(finding["control_mapping"] for finding in findings)


def test_risk_report_endpoint_returns_summary_and_synthetic_data_classification() -> None:
    client = TestClient(app)
    response = client.get("/risk-report")

    assert response.status_code == 200
    report = response.json()
    assert report["data_classification"] == "synthetic-demo-data-only"
    assert report["finding_counts_by_severity"]["high"] >= 8
    assert report["finding_counts_by_category"]["endpoint"] >= 4
    assert report["top_risky_assets"][0]["asset_id"] == "device-003"
    assert report["findings"]
