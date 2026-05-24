"""Tests for the static clickable demo export and assets."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.export_static_demo import build_static_demo_payload

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_static_demo_payload_contains_clickable_ui_data() -> None:
    payload = build_static_demo_payload()

    assert payload["data_classification"] == "synthetic-demo-data-only"
    assert payload["generated_at"] == "2026-05-22T12:00:00Z"
    assert {scenario["id"] for scenario in payload["scenarios"]} == {
        "failed-imaging",
        "disabled-user-device-assignment",
        "privileged-user-missing-mfa",
        "endpoint-compliance-queue",
    }
    assert any(device["hostname"] == "DEMO-WIN10-003" for device in payload["devices"])
    assert any(finding["asset_id"] == "device-003" for finding in payload["findings"])
    assert payload["summary"]["total_findings"] >= 10
    assert payload["vulnerability_records"]
    assert payload["patch_vulnerability_board"]
    assert payload["patch_vulnerability_board"][0]["severity"] == "critical"
    assert payload["remediation_queue"]
    assert payload["remediation_queue"][0]["ticket_id"] == "ticket-001"
    assert payload["risk_reduction_summary"]["open_ticket_count"] == 2
    assert payload["risk_reduction_summary"]["resolved_ticket_count"] == 1


def test_site_assets_exist_and_reference_demo_data() -> None:
    index = (SITE / "index.html").read_text(encoding="utf-8")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    styles = (SITE / "styles.css").read_text(encoding="utf-8")

    assert "Endpoint Identity Control Plane" in index
    assert "https://rblea97.github.io/endpoint-identity-control-plane/" in index
    assert "demo-data.json" in app
    assert "failed-imaging" in app
    assert "endpoint-compliance-queue" in app
    assert "owner-risk-list" in index
    assert "patch-vulnerability-board" in index
    assert "remediation-ticket-list" in index
    assert "risk-reduction-summary" in index
    assert "renderOwnerRisk" in app
    assert "renderPatchVulnerabilityBoard" in app
    assert "renderRemediationQueue" in app
    assert "renderRiskReduction" in app
    assert "--accent" in styles


def test_committed_demo_data_matches_export_shape() -> None:
    committed_payload = json.loads((SITE / "demo-data.json").read_text(encoding="utf-8"))
    regenerated_payload = build_static_demo_payload()

    assert committed_payload == regenerated_payload
