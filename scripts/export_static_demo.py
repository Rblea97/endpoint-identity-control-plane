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
        "findings": [finding.model_dump(mode="json") for finding in risk_report.findings],
        "top_risky_assets": [
            asset.model_dump(mode="json") for asset in risk_report.top_risky_assets
        ],
        "scenarios": scenarios,
    }


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
