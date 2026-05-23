"""Export synthetic endpoint/identity data for the static UI demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from endpoint_identity_control_plane.demo_data import load_demo_inventory
from endpoint_identity_control_plane.operations_demo import (
    DEMO_REPORT_AS_OF,
    build_scenario_report,
    list_scenarios,
)
from endpoint_identity_control_plane.risk import build_risk_report

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
OUTPUT_PATH = SITE_DIR / "demo-data.json"


def build_static_demo_payload() -> dict[str, Any]:
    """Build the JSON payload consumed by the static GitHub Pages demo."""
    inventory = load_demo_inventory()
    risk_report = build_risk_report(inventory, as_of=DEMO_REPORT_AS_OF)
    scenarios = [
        {
            "id": scenario.id,
            "title": scenario.title,
            "job_relevance": scenario.job_relevance,
            "report": build_scenario_report(scenario.id).__dict__,
        }
        for scenario in list_scenarios()
    ]

    return {
        "app_name": "Endpoint Identity Control Plane",
        "data_classification": inventory.data_classification,
        "generated_at": DEMO_REPORT_AS_OF.isoformat().replace("+00:00", "Z"),
        "summary": {
            "total_users": len(inventory.users),
            "total_devices": len(inventory.devices),
            "total_groups": len(inventory.groups),
            "total_findings": len(risk_report.findings),
            "severity_counts": risk_report.finding_counts_by_severity,
            "category_counts": risk_report.finding_counts_by_category,
        },
        "users": [user.model_dump(mode="json") for user in inventory.users],
        "devices": [device.model_dump(mode="json") for device in inventory.devices],
        "groups": [group.model_dump(mode="json") for group in inventory.groups],
        "vulnerability_records": [
            vulnerability.model_dump(mode="json")
            for vulnerability in inventory.vulnerability_records
        ],
        "patch_vulnerability_board": _build_patch_vulnerability_board(inventory),
        "remediation_queue": [
            item.model_dump(mode="json") for item in risk_report.remediation_queue
        ],
        "risk_reduction_summary": risk_report.risk_reduction_summary.model_dump(
            mode="json"
        ),
        "findings": [finding.model_dump(mode="json") for finding in risk_report.findings],
        "top_risky_assets": [
            asset.model_dump(mode="json") for asset in risk_report.top_risky_assets
        ],
        "scenarios": scenarios,
    }


def _build_patch_vulnerability_board(inventory: Any) -> list[dict[str, Any]]:
    users_by_id = {user.id: user for user in inventory.users}
    devices_by_id = {device.id: device for device in inventory.devices}
    board: list[dict[str, Any]] = []

    for vulnerability in inventory.vulnerability_records:
        device = devices_by_id[vulnerability.device_id]
        owner = users_by_id[device.assigned_user_id]
        board.append(
            {
                "vulnerability_id": vulnerability.id,
                "device_id": device.id,
                "hostname": device.hostname,
                "owner_username": owner.username,
                "owner_privileged": bool(owner.privileged_groups),
                "title": vulnerability.title,
                "severity": vulnerability.severity,
                "status": vulnerability.status,
                "patch_available": vulnerability.patch_available,
                "recommended_action": vulnerability.recommended_action,
            }
        )

    return sorted(
        board,
        key=lambda item: (
            item["status"] == "open",
            SEVERITY_ORDER[item["severity"]],
            item["owner_privileged"],
            item["vulnerability_id"],
        ),
        reverse=True,
    )


def export_static_demo(output_path: Path = OUTPUT_PATH) -> Path:
    """Write the static demo JSON payload to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_static_demo_payload()
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def main() -> int:
    """Export the static demo payload and print the output path."""
    output_path = export_static_demo()
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
