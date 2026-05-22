from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from endpoint_identity_control_plane.demo_data import DEMO_INVENTORY_PATH, load_demo_inventory
from endpoint_identity_control_plane.models import Inventory


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


def test_loader_rejects_fixture_text_with_secret_markers(tmp_path: Path) -> None:
    data = json.loads(DEMO_INVENTORY_PATH.read_text(encoding="utf-8"))
    data["source"] = "contains password marker"
    unsafe_fixture = tmp_path / "unsafe-inventory.json"
    unsafe_fixture.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="secret-like marker"):
        load_demo_inventory(unsafe_fixture)
