"""Actionable IT operations demo scenarios for the synthetic lab."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from endpoint_identity_control_plane.demo_data import load_demo_inventory
from endpoint_identity_control_plane.models import Device, Inventory, User
from endpoint_identity_control_plane.risk import Finding, evaluate_inventory

DEMO_REPORT_AS_OF = datetime(2026, 5, 22, 12, 0, tzinfo=UTC)


class UnknownScenarioError(ValueError):
    """Raised when a requested demo scenario does not exist."""

    def __init__(self, scenario_id: str, valid_scenarios: Sequence[str]) -> None:
        """Build a helpful unknown-scenario message."""
        valid = ", ".join(valid_scenarios)
        super().__init__(f"unknown scenario: {scenario_id}; valid scenarios: {valid}")


@dataclass(frozen=True)
class ScenarioMetadata:
    """Metadata for an actionable IT demo scenario."""

    id: str
    title: str
    job_relevance: str


@dataclass(frozen=True)
class ScenarioReport:
    """Technician-facing scenario report rendered by the demo CLI."""

    scenario_id: str
    title: str
    ticket: str
    job_relevance: str
    affected_assets: list[str]
    findings: list[str]
    technician_actions: list[str]
    verification_steps: list[str]

    def render(self) -> str:
        """Render the report as readable terminal text."""
        sections = [
            f"Scenario: {self.title}",
            f"Scenario ID: {self.scenario_id}",
            "",
            "Ticket:",
            f"- {self.ticket}",
            "",
            "Why this maps to IT work:",
            f"- {self.job_relevance}",
            "",
            "Affected assets:",
            *_render_bullets(self.affected_assets),
            "",
            "Findings:",
            *_render_bullets(self.findings),
            "",
            "Technician actions:",
            *_render_numbered(self.technician_actions),
            "",
            "Verification:",
            *_render_numbered(self.verification_steps),
        ]
        return "\n".join(sections)


_SCENARIOS = (
    ScenarioMetadata(
        id="failed-imaging",
        title="Failed imaging / endpoint provisioning triage",
        job_relevance=(
            "Practices the SCCM/MECM-style thought process of checking deployment state, "
            "agent check-in, compliance, encryption, and patch readiness before closing a "
            "new laptop imaging ticket."
        ),
    ),
    ScenarioMetadata(
        id="disabled-user-device-assignment",
        title="Disabled user still assigned to device",
        job_relevance=(
            "Practices Active Directory and endpoint lifecycle hygiene: disabled users should "
            "not keep active device ownership without review, reclaim, or reassignment."
        ),
    ),
    ScenarioMetadata(
        id="privileged-user-missing-mfa",
        title="Privileged identity missing MFA",
        job_relevance=(
            "Practices identity administration escalation: privileged access should have MFA "
            "and group membership should be reviewed before access is trusted."
        ),
    ),
    ScenarioMetadata(
        id="endpoint-compliance-queue",
        title="Endpoint compliance remediation queue",
        job_relevance=(
            "Practices prioritizing endpoint support work by risk, evidence, and remediation "
            "steps instead of treating all device issues as equal."
        ),
    ),
)


def list_scenarios() -> list[ScenarioMetadata]:
    """Return supported actionable IT demo scenarios."""
    return list(_SCENARIOS)


def build_scenario_report(scenario_id: str) -> ScenarioReport:
    """Build a technician-facing report for one supported scenario."""
    metadata = _scenario_metadata(scenario_id)
    inventory = load_demo_inventory()
    findings = evaluate_inventory(inventory, as_of=DEMO_REPORT_AS_OF)

    if scenario_id == "failed-imaging":
        return _failed_imaging_report(metadata, inventory, findings)
    if scenario_id == "disabled-user-device-assignment":
        return _disabled_user_device_assignment_report(metadata, inventory, findings)
    if scenario_id == "privileged-user-missing-mfa":
        return _privileged_user_missing_mfa_report(metadata, inventory, findings)
    if scenario_id == "endpoint-compliance-queue":
        return _endpoint_compliance_queue_report(metadata, inventory, findings)

    valid_scenarios = [scenario.id for scenario in _SCENARIOS]
    raise UnknownScenarioError(scenario_id, valid_scenarios)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the operations demo CLI."""
    parser = argparse.ArgumentParser(
        prog="endpoint-identity-demo",
        description="Run synthetic endpoint and identity IT operations demo scenarios.",
    )
    parser.add_argument("--list", action="store_true", help="List supported demo scenarios.")
    parser.add_argument("--scenario", help="Run a specific demo scenario by ID.")
    args = parser.parse_args(argv)

    if args.list:
        for scenario in list_scenarios():
            print(f"{scenario.id}: {scenario.title}")
        return 0

    if args.scenario:
        try:
            print(build_scenario_report(args.scenario).render())
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0

    parser.print_help()
    return 0


def _scenario_metadata(scenario_id: str) -> ScenarioMetadata:
    for scenario in _SCENARIOS:
        if scenario.id == scenario_id:
            return scenario
    valid_scenarios = [scenario.id for scenario in _SCENARIOS]
    raise UnknownScenarioError(scenario_id, valid_scenarios)


def _failed_imaging_report(
    metadata: ScenarioMetadata, inventory: Inventory, findings: list[Finding]
) -> ScenarioReport:
    device = _device_by_id(inventory, "device-003")
    device_findings = _findings_for_asset(findings, asset_id=device.id)
    return ScenarioReport(
        scenario_id=metadata.id,
        title=metadata.title,
        ticket="User reports a newly imaged laptop is not ready for use.",
        job_relevance=metadata.job_relevance,
        affected_assets=[device.hostname],
        findings=_format_findings(device_findings),
        technician_actions=[
            "Confirm the device record exists in endpoint inventory or SCCM/MECM.",
            "Review deployment logs for the failed imaging or task sequence state.",
            "Confirm the endpoint checks in successfully after remediation.",
            "Validate encryption, compliance, and patch visibility before handoff.",
            "Update the ticket with findings, action taken, and verification evidence.",
        ],
        verification_steps=[
            "Imaging state is complete or a reimage path is documented.",
            "Device check-in is current and visible to endpoint tooling.",
            "Encryption and compliance state are acceptable for user handoff.",
        ],
    )


def _disabled_user_device_assignment_report(
    metadata: ScenarioMetadata, inventory: Inventory, findings: list[Finding]
) -> ScenarioReport:
    user = _user_by_id(inventory, "user-003")
    device = _device_by_id(inventory, user.assigned_device_ids[0])
    user_findings = _findings_for_asset(findings, asset_id=user.id)
    return ScenarioReport(
        scenario_id=metadata.id,
        title=metadata.title,
        ticket="Offboarding review finds a disabled user still assigned to a laptop.",
        job_relevance=metadata.job_relevance,
        affected_assets=[user.username, device.hostname],
        findings=_format_findings(user_findings),
        technician_actions=[
            "Confirm the account is disabled and identify the assigned endpoint.",
            "Check whether the device should be reclaimed, reassigned, or retired.",
            "Remove stale ownership notes after manager or asset approval.",
            "Document the offboarding cleanup in the ticket.",
        ],
        verification_steps=[
            "Disabled user no longer owns active endpoint assignments without review.",
            "Device ownership and asset lifecycle status are documented.",
        ],
    )


def _privileged_user_missing_mfa_report(
    metadata: ScenarioMetadata, inventory: Inventory, findings: list[Finding]
) -> ScenarioReport:
    user = _user_by_id(inventory, "user-002")
    user_findings = _findings_for_asset(findings, asset_id=user.id)
    return ScenarioReport(
        scenario_id=metadata.id,
        title=metadata.title,
        ticket="Identity review flags a privileged account without MFA enabled.",
        job_relevance=metadata.job_relevance,
        affected_assets=[user.username],
        findings=_format_findings(user_findings),
        technician_actions=[
            "Confirm privileged group membership and business need.",
            "Escalate or enable MFA according to identity policy.",
            "Review whether local or endpoint admin access is still required.",
            "Document the identity hygiene remediation or exception.",
        ],
        verification_steps=[
            "MFA is enabled or an approved exception is recorded.",
            "Privileged group membership has a documented owner and purpose.",
        ],
    )


def _endpoint_compliance_queue_report(
    metadata: ScenarioMetadata, inventory: Inventory, findings: list[Finding]
) -> ScenarioReport:
    endpoint_rows: list[tuple[Device, list[Finding]]] = []
    for device in inventory.devices:
        device_findings = _findings_for_asset(findings, asset_id=device.id)
        if device_findings:
            endpoint_rows.append((device, device_findings))

    endpoint_rows = sorted(
        endpoint_rows,
        key=lambda row: (
            len(row[1]),
            max(_severity_rank(finding.severity) for finding in row[1]),
            row[0].hostname,
        ),
        reverse=True,
    )
    affected_assets = [device.hostname for device, _device_findings in endpoint_rows]
    endpoint_summaries = []
    for device, device_findings in endpoint_rows:
        highest = max(device_findings, key=lambda finding: _severity_rank(finding.severity))
        endpoint_summaries.append(
            f"{device.hostname}: {len(device_findings)} findings, "
            f"highest severity {highest.severity}"
        )

    return ScenarioReport(
        scenario_id=metadata.id,
        title=metadata.title,
        ticket="Endpoint support queue needs a prioritized remediation plan.",
        job_relevance=metadata.job_relevance,
        affected_assets=affected_assets,
        findings=endpoint_summaries,
        technician_actions=[
            "Prioritize devices with the most findings and highest severity first.",
            "Start with compliance blockers: encryption, patch visibility, and policy state.",
            "Separate quick fixes from devices that need reimage, owner review, or escalation.",
            "Record remediation evidence before closing endpoint tickets.",
        ],
        verification_steps=[
            "Highest-risk devices have an owner, next action, and expected resolution path.",
            "Compliance-impacting findings are remediated or escalated.",
        ],
    )


def _findings_for_asset(findings: list[Finding], *, asset_id: str) -> list[Finding]:
    return [finding for finding in findings if finding.asset_id == asset_id]


def _format_findings(findings: list[Finding]) -> list[str]:
    return [
        f"{finding.severity.upper()} {finding.category}: {finding.title} — {finding.recommendation}"
        for finding in findings
    ]


def _device_by_id(inventory: Inventory, device_id: str) -> Device:
    for device in inventory.devices:
        if device.id == device_id:
            return device
    raise KeyError(device_id)


def _user_by_id(inventory: Inventory, user_id: str) -> User:
    return inventory.user_by_id(user_id)


def _render_bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _render_numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, start=1)]


def _severity_rank(severity: str) -> int:
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}[severity]


if __name__ == "__main__":
    raise SystemExit(main())
