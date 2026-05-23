from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from endpoint_identity_control_plane.demo_data import DEMO_INVENTORY_PATH, load_demo_inventory
from endpoint_identity_control_plane.models import Inventory
from endpoint_identity_control_plane.risk import evaluate_inventory

AS_OF = datetime(2026, 5, 22, 12, 0, tzinfo=UTC)


def test_load_demo_inventory_returns_typed_synthetic_inventory() -> None:
    inventory = load_demo_inventory()

    assert isinstance(inventory, Inventory)
    assert len(inventory.users) >= 3
    assert len(inventory.devices) >= 3
    assert len(inventory.groups) >= 2
    assert inventory.data_classification == "synthetic-demo-data-only"
    assert inventory.source == "committed-demo-fixture"


def test_demo_inventory_relationships_are_consistent() -> None:
    inventory = load_demo_inventory()

    user_ids = {user.id for user in inventory.users}
    device_ids = {device.id for device in inventory.devices}
    group_ids = {group.id for group in inventory.groups}
    finding_ids = {finding.id for finding in evaluate_inventory(inventory, as_of=AS_OF)}

    for user in inventory.users:
        assert set(user.assigned_device_ids) <= device_ids
        assert set(user.privileged_groups) <= group_ids

    for device in inventory.devices:
        assert device.assigned_user_id in user_ids
        assigned_user = inventory.user_by_id(device.assigned_user_id)
        assert device.id in assigned_user.assigned_device_ids

    for group in inventory.groups:
        assert set(group.member_user_ids) <= user_ids
        for member_user_id in group.member_user_ids:
            member = inventory.user_by_id(member_user_id)
            if group.privilege_level in {"admin", "tier0"}:
                assert group.id in member.privileged_groups

    for vulnerability in inventory.vulnerability_records:
        assert vulnerability.device_id in device_ids

    for ticket in inventory.remediation_tickets:
        if ticket.asset_type == "user":
            assert ticket.asset_id in user_ids
        if ticket.asset_type == "device":
            assert ticket.asset_id in device_ids
        if ticket.asset_type == "group":
            assert ticket.asset_id in group_ids
        assert set(ticket.linked_finding_ids) <= finding_ids


def test_open_remediation_tickets_link_active_risk_findings() -> None:
    inventory = load_demo_inventory()
    active_finding_ids = {finding.id for finding in evaluate_inventory(inventory, as_of=AS_OF)}

    for ticket in inventory.remediation_tickets:
        if ticket.status == "resolved":
            continue
        assert set(ticket.linked_finding_ids) & active_finding_ids


def test_demo_inventory_includes_vulnerability_and_remediation_records() -> None:
    inventory = load_demo_inventory()

    assert len(inventory.vulnerability_records) >= 3
    assert len(inventory.remediation_tickets) >= 3
    assert any(vulnerability.status == "open" for vulnerability in inventory.vulnerability_records)
    assert any(ticket.status == "resolved" for ticket in inventory.remediation_tickets)
    assert any(ticket.linked_finding_ids for ticket in inventory.remediation_tickets)


def test_demo_fixture_uses_fake_data_and_contains_no_secret_markers() -> None:
    raw_fixture = DEMO_INVENTORY_PATH.read_text(encoding="utf-8").lower()
    inventory = load_demo_inventory()

    assert "synthetic-demo-data-only" in raw_fixture
    assert ".example" in raw_fixture
    assert "contoso" not in raw_fixture
    assert "password" not in raw_fixture
    assert "secret" not in raw_fixture
    assert "token" not in raw_fixture
    assert "tenant_id" not in raw_fixture
    assert all(user.username.endswith(".example") for user in inventory.users)
    assert all(device.hostname.startswith("DEMO-") for device in inventory.devices)


def test_inventory_rejects_unknown_device_assignment() -> None:
    data = json.loads(DEMO_INVENTORY_PATH.read_text(encoding="utf-8"))
    data["users"][0]["assigned_device_ids"].append("device-missing")

    with pytest.raises(ValidationError, match="assigned_device_ids"):
        Inventory.model_validate(data)


def test_inventory_rejects_unknown_vulnerability_device_reference() -> None:
    data = json.loads(DEMO_INVENTORY_PATH.read_text(encoding="utf-8"))
    data["vulnerability_records"][0]["device_id"] = "device-missing"

    with pytest.raises(ValidationError, match="vulnerability"):
        Inventory.model_validate(data)


def test_inventory_rejects_unknown_remediation_asset_reference() -> None:
    data = json.loads(DEMO_INVENTORY_PATH.read_text(encoding="utf-8"))
    data["remediation_tickets"][0]["asset_id"] = "device-missing"

    with pytest.raises(ValidationError, match="remediation"):
        Inventory.model_validate(data)


def test_loader_rejects_fixture_text_with_secret_markers(tmp_path: Path) -> None:
    data = json.loads(DEMO_INVENTORY_PATH.read_text(encoding="utf-8"))
    data["source"] = "contains password marker"
    unsafe_fixture = tmp_path / "unsafe-inventory.json"
    unsafe_fixture.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="secret-like marker"):
        load_demo_inventory(unsafe_fixture)
