from datetime import UTC, datetime

from endpoint_identity_control_plane.demo_data import load_demo_inventory
from endpoint_identity_control_plane.risk import build_risk_report, evaluate_inventory

AS_OF = datetime(2026, 5, 22, 12, 0, tzinfo=UTC)


def test_evaluate_inventory_returns_expected_demo_findings() -> None:
    inventory = load_demo_inventory()
    findings = evaluate_inventory(inventory, as_of=AS_OF)
    finding_ids = {finding.id for finding in findings}

    assert "identity-privileged-user-missing-mfa-user-002" in finding_ids
    assert "lifecycle-disabled-user-assigned-device-user-003" in finding_ids
    assert "identity-stale-user-login-user-003" in finding_ids
    assert "endpoint-stale-device-checkin-device-003" in finding_ids
    assert "endpoint-unsupported-os-device-003" in finding_ids
    assert "endpoint-encryption-disabled-device-003" in finding_ids
    assert "endpoint-local-admin-exposure-device-002" in finding_ids
    assert "endpoint-local-admin-exposure-device-003" in finding_ids
    assert "compliance-noncompliant-endpoint-device-002" in finding_ids
    assert "imaging-incomplete-state-device-003" in finding_ids
    assert "imaging-incomplete-state-device-004" in finding_ids
    assert "compliance-patch-status-device-003" in finding_ids
    assert "compliance-patch-status-device-004" in finding_ids


def test_findings_include_evidence_recommendation_and_control_mapping() -> None:
    inventory = load_demo_inventory()
    findings = evaluate_inventory(inventory, as_of=AS_OF)

    assert findings
    assert all(finding.title for finding in findings)
    assert all(finding.evidence for finding in findings)
    assert all(finding.recommendation for finding in findings)
    assert all(finding.control_mapping for finding in findings)
    assert all(finding.asset_id for finding in findings)


def test_risk_report_summarizes_findings_by_severity_and_category() -> None:
    inventory = load_demo_inventory()
    report = build_risk_report(inventory, as_of=AS_OF)

    assert report.generated_at == AS_OF
    assert report.data_classification == "synthetic-demo-data-only"
    assert report.finding_counts_by_severity["high"] >= 8
    assert report.finding_counts_by_severity["medium"] >= 3
    assert report.finding_counts_by_category["endpoint"] >= 4
    assert report.finding_counts_by_category["identity"] >= 2
    assert report.findings


def test_risk_report_identifies_top_risky_assets() -> None:
    inventory = load_demo_inventory()
    report = build_risk_report(inventory, as_of=AS_OF)

    assert report.top_risky_assets
    top_asset = report.top_risky_assets[0]
    assert top_asset.asset_type == "device"
    assert top_asset.asset_id == "device-003"
    assert top_asset.finding_count >= 5
    assert top_asset.highest_severity == "high"


def test_open_vulnerabilities_create_deterministic_findings() -> None:
    inventory = load_demo_inventory()
    findings = evaluate_inventory(inventory, as_of=AS_OF)
    finding_ids = {finding.id for finding in findings}

    assert "vulnerability-open-vuln-001" in finding_ids
    assert "vulnerability-open-vuln-002" in finding_ids
    assert "vulnerability-open-vuln-004" not in finding_ids


def test_privileged_owner_endpoint_risk_is_correlated() -> None:
    inventory = load_demo_inventory()
    findings = evaluate_inventory(inventory, as_of=AS_OF)
    correlated = next(
        finding
        for finding in findings
        if finding.id == "identity-endpoint-correlation-device-002-user-002"
    )

    assert correlated.severity == "critical"
    assert correlated.asset_type == "device"
    assert correlated.asset_id == "device-002"
    assert correlated.evidence["owner_username"] == "jamie.chen@example.example"
    assert correlated.evidence["privileged_group_count"] == 1


def test_risk_report_includes_remediation_queue_and_risk_reduction() -> None:
    inventory = load_demo_inventory()
    report = build_risk_report(inventory, as_of=AS_OF)

    assert report.remediation_queue
    assert report.remediation_queue[0].ticket_id == "ticket-001"
    assert report.remediation_queue[0].priority == "critical"
    assert report.risk_reduction_summary.open_ticket_count == 2
    assert report.risk_reduction_summary.resolved_ticket_count == 1
    assert (
        report.risk_reduction_summary.active_risk_points
        > report.risk_reduction_summary.resolved_risk_points
    )


def test_risk_evaluation_is_deterministic_for_same_as_of() -> None:
    inventory = load_demo_inventory()

    first = evaluate_inventory(inventory, as_of=AS_OF)
    second = evaluate_inventory(inventory, as_of=AS_OF)

    assert [finding.model_dump() for finding in first] == [
        finding.model_dump() for finding in second
    ]
