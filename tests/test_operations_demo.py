"""Tests for actionable IT operations demo scenarios."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from endpoint_identity_control_plane.operations_demo import (
    build_scenario_report,
    list_scenarios,
    main,
)


def test_lists_actionable_it_demo_scenarios() -> None:
    scenarios = list_scenarios()

    assert [scenario.id for scenario in scenarios] == [
        "failed-imaging",
        "disabled-user-device-assignment",
        "privileged-user-missing-mfa",
        "endpoint-compliance-queue",
    ]
    assert all(scenario.title for scenario in scenarios)
    assert all(scenario.job_relevance for scenario in scenarios)


def test_failed_imaging_report_reads_like_it_triage() -> None:
    report = build_scenario_report("failed-imaging")

    assert report.scenario_id == "failed-imaging"
    assert report.title == "Failed imaging / endpoint provisioning triage"
    assert "newly imaged laptop" in report.ticket.lower()
    assert report.affected_assets == ["DEMO-WIN10-003"]
    assert any("imaging" in finding.lower() for finding in report.findings)
    assert any("stale" in finding.lower() for finding in report.findings)
    assert any("deployment logs" in action.lower() for action in report.technician_actions)
    assert any("ticket" in action.lower() for action in report.technician_actions)
    rendered = report.render()
    assert "Scenario: Failed imaging / endpoint provisioning triage" in rendered
    assert "Affected assets:" in rendered
    assert "Technician actions:" in rendered
    assert "DEMO-WIN10-003" in rendered


def test_disabled_user_device_assignment_report_maps_to_offboarding() -> None:
    report = build_scenario_report("disabled-user-device-assignment")

    assert report.affected_assets == ["taylor.morgan@example.example", "DEMO-WIN10-003"]
    assert "offboarding" in report.ticket.lower()
    assert any("disabled" in finding.lower() for finding in report.findings)
    assert any("reclaim" in action.lower() for action in report.technician_actions)


def test_endpoint_compliance_queue_prioritizes_top_endpoint() -> None:
    report = build_scenario_report("endpoint-compliance-queue")

    assert report.affected_assets[0] == "DEMO-WIN10-003"
    assert any("6 findings" in finding for finding in report.findings)
    assert any("prioritize" in action.lower() for action in report.technician_actions)
    assert any("compliance" in action.lower() for action in report.technician_actions)


def test_cli_lists_scenarios(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--list"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "failed-imaging" in captured.out
    assert "endpoint-compliance-queue" in captured.out


def test_cli_renders_failed_imaging_report(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--scenario", "failed-imaging"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Scenario: Failed imaging / endpoint provisioning triage" in captured.out
    assert "DEMO-WIN10-003" in captured.out
    assert "Technician actions:" in captured.out


def test_pyproject_exposes_demo_console_script() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"] == {
        "endpoint-identity-demo": "endpoint_identity_control_plane.operations_demo:main"
    }


def test_unknown_scenario_raises_helpful_error() -> None:
    with pytest.raises(ValueError, match="unknown scenario"):
        build_scenario_report("not-a-scenario")
