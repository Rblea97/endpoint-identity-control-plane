"""Deterministic endpoint and identity risk evaluation."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from endpoint_identity_control_plane.models import Device, Inventory, User

Severity = Literal["low", "medium", "high", "critical"]
FindingCategory = Literal["identity", "endpoint", "compliance", "lifecycle", "imaging"]
AssetType = Literal["user", "device", "group"]

STALE_USER_DAYS = 60
STALE_DEVICE_DAYS = 30
MAX_EXPECTED_LOCAL_ADMINS = 1


class Finding(BaseModel):
    """A deterministic endpoint or identity risk finding."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1)
    severity: Severity
    category: FindingCategory
    title: str = Field(min_length=1)
    asset_type: AssetType
    asset_id: str = Field(min_length=1)
    evidence: dict[str, str | int | bool | None]
    recommendation: str = Field(min_length=1)
    control_mapping: str = Field(min_length=1)


class AssetRiskSummary(BaseModel):
    """Summary of finding volume for one asset."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    asset_type: AssetType
    asset_id: str = Field(min_length=1)
    finding_count: int = Field(ge=0)
    highest_severity: Severity


class RiskReport(BaseModel):
    """Prioritized synthetic risk report."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    generated_at: datetime
    data_classification: Literal["synthetic-demo-data-only"]
    finding_counts_by_severity: dict[Severity, int]
    finding_counts_by_category: dict[FindingCategory, int]
    top_risky_assets: list[AssetRiskSummary]
    findings: list[Finding]


def evaluate_inventory(inventory: Inventory, *, as_of: datetime) -> list[Finding]:
    """Evaluate all v1 endpoint and identity risk rules."""
    findings: list[Finding] = []

    for user in inventory.users:
        findings.extend(_evaluate_user(user, as_of=as_of))

    for device in inventory.devices:
        findings.extend(_evaluate_device(device, as_of=as_of))

    return sorted(
        findings, key=lambda finding: (_severity_rank(finding.severity), finding.id), reverse=True
    )


def build_risk_report(inventory: Inventory, *, as_of: datetime) -> RiskReport:
    """Build a summarized risk report for validated synthetic inventory."""
    findings = evaluate_inventory(inventory, as_of=as_of)
    severity_counts: Counter[Severity] = Counter(finding.severity for finding in findings)
    category_counts: Counter[FindingCategory] = Counter(finding.category for finding in findings)

    return RiskReport(
        generated_at=as_of,
        data_classification=inventory.data_classification,
        finding_counts_by_severity=dict(severity_counts),
        finding_counts_by_category=dict(category_counts),
        top_risky_assets=_top_risky_assets(findings),
        findings=findings,
    )


def _evaluate_user(user: User, *, as_of: datetime) -> list[Finding]:
    findings: list[Finding] = []

    if user.privileged_groups and not user.mfa_enabled:
        findings.append(
            Finding(
                id=f"identity-privileged-user-missing-mfa-{user.id}",
                severity="high",
                category="identity",
                title="Privileged user does not have MFA enabled",
                asset_type="user",
                asset_id=user.id,
                evidence={
                    "username": user.username,
                    "privileged_group_count": len(user.privileged_groups),
                    "mfa_enabled": user.mfa_enabled,
                },
                recommendation="Require MFA for privileged endpoint or identity access.",
                control_mapping="Identity hygiene: privileged access protection",
            )
        )

    if not user.enabled and user.assigned_device_ids:
        findings.append(
            Finding(
                id=f"lifecycle-disabled-user-assigned-device-{user.id}",
                severity="high",
                category="lifecycle",
                title="Disabled user still has assigned devices",
                asset_type="user",
                asset_id=user.id,
                evidence={
                    "username": user.username,
                    "assigned_device_count": len(user.assigned_device_ids),
                },
                recommendation="Review offboarding and reclaim or reassign the user's devices.",
                control_mapping="Lifecycle hygiene: offboarding and asset ownership",
            )
        )

    if user.last_login_at is not None:
        stale_days = (as_of - user.last_login_at).days
        if stale_days > STALE_USER_DAYS:
            findings.append(
                Finding(
                    id=f"identity-stale-user-login-{user.id}",
                    severity="medium",
                    category="identity",
                    title="User login is stale",
                    asset_type="user",
                    asset_id=user.id,
                    evidence={"username": user.username, "days_since_login": stale_days},
                    recommendation="Review account need and disable it if unused.",
                    control_mapping="Identity hygiene: stale account review",
                )
            )

    return findings


def _evaluate_device(device: Device, *, as_of: datetime) -> list[Finding]:
    findings: list[Finding] = []

    if device.last_checkin_at is not None:
        stale_days = (as_of - device.last_checkin_at).days
        if stale_days > STALE_DEVICE_DAYS:
            findings.append(
                Finding(
                    id=f"endpoint-stale-device-checkin-{device.id}",
                    severity="medium",
                    category="endpoint",
                    title="Device check-in is stale",
                    asset_type="device",
                    asset_id=device.id,
                    evidence={"hostname": device.hostname, "days_since_checkin": stale_days},
                    recommendation="Confirm ownership, network reachability, and agent health.",
                    control_mapping="Endpoint hygiene: device inventory freshness",
                )
            )

    if "windows 10" in device.os_name.lower():
        findings.append(
            Finding(
                id=f"endpoint-unsupported-os-{device.id}",
                severity="high",
                category="endpoint",
                title="Device is running an unsupported OS baseline for this demo",
                asset_type="device",
                asset_id=device.id,
                evidence={
                    "hostname": device.hostname,
                    "os_name": device.os_name,
                    "os_version": device.os_version,
                },
                recommendation="Plan OS upgrade or replacement before relying on the endpoint.",
                control_mapping="Endpoint hygiene: supported operating system baseline",
            )
        )

    if not device.encryption_enabled:
        findings.append(
            Finding(
                id=f"endpoint-encryption-disabled-{device.id}",
                severity="high",
                category="endpoint",
                title="Endpoint encryption is disabled",
                asset_type="device",
                asset_id=device.id,
                evidence={
                    "hostname": device.hostname,
                    "encryption_enabled": device.encryption_enabled,
                },
                recommendation="Enable disk encryption or quarantine the device until remediated.",
                control_mapping="Endpoint protection: disk encryption",
            )
        )

    if device.local_admin_count > MAX_EXPECTED_LOCAL_ADMINS:
        findings.append(
            Finding(
                id=f"endpoint-local-admin-exposure-{device.id}",
                severity="high",
                category="endpoint",
                title="Endpoint has excessive local administrator exposure",
                asset_type="device",
                asset_id=device.id,
                evidence={
                    "hostname": device.hostname,
                    "local_admin_count": device.local_admin_count,
                    "expected_maximum": MAX_EXPECTED_LOCAL_ADMINS,
                },
                recommendation="Remove unnecessary local administrator access.",
                control_mapping="Endpoint protection: least privilege",
            )
        )

    if device.compliance_state == "noncompliant":
        findings.append(
            Finding(
                id=f"compliance-noncompliant-endpoint-{device.id}",
                severity="high",
                category="compliance",
                title="Endpoint is noncompliant",
                asset_type="device",
                asset_id=device.id,
                evidence={"hostname": device.hostname, "compliance_state": device.compliance_state},
                recommendation="Review failed policies and remediate before granting access.",
                control_mapping="Compliance hygiene: endpoint policy enforcement",
            )
        )

    if device.imaging_state in {"failed", "in_progress"}:
        severity: Severity = "high" if device.imaging_state == "failed" else "medium"
        findings.append(
            Finding(
                id=f"imaging-incomplete-state-{device.id}",
                severity=severity,
                category="imaging",
                title="Endpoint imaging state requires review",
                asset_type="device",
                asset_id=device.id,
                evidence={"hostname": device.hostname, "imaging_state": device.imaging_state},
                recommendation="Review deployment logs and confirm provisioning completed.",
                control_mapping="Endpoint lifecycle: imaging and provisioning quality",
            )
        )

    if device.patch_status in {"missing", "unknown"}:
        severity = "high" if device.patch_status == "missing" else "medium"
        findings.append(
            Finding(
                id=f"compliance-patch-status-{device.id}",
                severity=severity,
                category="compliance",
                title="Endpoint patch status requires review",
                asset_type="device",
                asset_id=device.id,
                evidence={"hostname": device.hostname, "patch_status": device.patch_status},
                recommendation="Confirm patch scan health and apply missing updates if needed.",
                control_mapping="Compliance hygiene: patch visibility",
            )
        )

    return findings


def _top_risky_assets(findings: list[Finding]) -> list[AssetRiskSummary]:
    grouped: dict[tuple[AssetType, str], list[Finding]] = {}
    for finding in findings:
        grouped.setdefault((finding.asset_type, finding.asset_id), []).append(finding)

    summaries = [
        AssetRiskSummary(
            asset_type=asset_type,
            asset_id=asset_id,
            finding_count=len(asset_findings),
            highest_severity=max(
                (finding.severity for finding in asset_findings), key=_severity_rank
            ),
        )
        for (asset_type, asset_id), asset_findings in grouped.items()
    ]
    return sorted(
        summaries,
        key=lambda summary: (
            summary.finding_count,
            _severity_rank(summary.highest_severity),
            summary.asset_id,
        ),
        reverse=True,
    )


def _severity_rank(severity: Severity) -> int:
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}[severity]
