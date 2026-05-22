"""Pydantic models for synthetic endpoint and identity inventory."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

ComplianceState = Literal["compliant", "noncompliant", "unknown"]
ImagingState = Literal["complete", "in_progress", "failed", "unknown"]
PatchStatus = Literal["current", "behind", "missing", "unknown"]
PrivilegeLevel = Literal["standard", "admin", "tier0"]


class StrictInventoryModel(BaseModel):
    """Base model for synthetic inventory records."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class User(StrictInventoryModel):
    """Synthetic identity record."""

    id: str = Field(min_length=1)
    username: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    enabled: bool
    last_login_at: datetime | None
    mfa_enabled: bool
    privileged_groups: list[str] = Field(default_factory=list)
    assigned_device_ids: list[str] = Field(default_factory=list)


class Device(StrictInventoryModel):
    """Synthetic Windows endpoint record."""

    id: str = Field(min_length=1)
    hostname: str = Field(min_length=1)
    assigned_user_id: str = Field(min_length=1)
    os_name: str = Field(min_length=1)
    os_version: str = Field(min_length=1)
    last_checkin_at: datetime | None
    patch_status: PatchStatus
    encryption_enabled: bool
    local_admin_count: int = Field(ge=0)
    compliance_state: ComplianceState
    imaging_state: ImagingState


class Group(StrictInventoryModel):
    """Synthetic identity group record."""

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    privilege_level: PrivilegeLevel
    member_user_ids: list[str] = Field(default_factory=list)


class Inventory(StrictInventoryModel):
    """Validated synthetic users, devices, and groups."""

    data_classification: Literal["synthetic-demo-data-only"]
    source: Literal["committed-demo-fixture"]
    users: list[User]
    devices: list[Device]
    groups: list[Group]

    @model_validator(mode="after")
    def validate_relationships(self) -> Self:
        """Ensure committed inventory references only known records."""
        user_ids = {user.id for user in self.users}
        device_ids = {device.id for device in self.devices}
        group_ids = {group.id for group in self.groups}

        self._validate_unique_ids("users", [user.id for user in self.users])
        self._validate_unique_ids("devices", [device.id for device in self.devices])
        self._validate_unique_ids("groups", [group.id for group in self.groups])

        for user in self.users:
            unknown_devices = sorted(set(user.assigned_device_ids) - device_ids)
            if unknown_devices:
                message = (
                    f"user {user.id} assigned_device_ids reference unknown devices: "
                    f"{', '.join(unknown_devices)}"
                )
                raise ValueError(message)

            unknown_groups = sorted(set(user.privileged_groups) - group_ids)
            if unknown_groups:
                message = (
                    f"user {user.id} privileged_groups reference unknown groups: "
                    f"{', '.join(unknown_groups)}"
                )
                raise ValueError(message)

        for device in self.devices:
            if device.assigned_user_id not in user_ids:
                message = (
                    f"device {device.id} assigned_user_id references unknown user: "
                    f"{device.assigned_user_id}"
                )
                raise ValueError(message)

            assigned_user = self.user_by_id(device.assigned_user_id)
            if device.id not in assigned_user.assigned_device_ids:
                message = (
                    f"device {device.id} is assigned to {assigned_user.id}, "
                    "but that user does not list the device"
                )
                raise ValueError(message)

        for group in self.groups:
            unknown_members = sorted(set(group.member_user_ids) - user_ids)
            if unknown_members:
                message = (
                    f"group {group.id} member_user_ids reference unknown users: "
                    f"{', '.join(unknown_members)}"
                )
                raise ValueError(message)

            if group.privilege_level in {"admin", "tier0"}:
                self._validate_privileged_group_membership(group)

        return self

    def user_by_id(self, user_id: str) -> User:
        """Return a user by id."""
        for user in self.users:
            if user.id == user_id:
                return user
        raise KeyError(user_id)

    @staticmethod
    def _validate_unique_ids(label: str, ids: list[str]) -> None:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for item_id in ids:
            if item_id in seen:
                duplicates.add(item_id)
            seen.add(item_id)

        if duplicates:
            message = f"{label} contains duplicate ids: {', '.join(sorted(duplicates))}"
            raise ValueError(message)

    def _validate_privileged_group_membership(self, group: Group) -> None:
        for member_user_id in group.member_user_ids:
            member = self.user_by_id(member_user_id)
            if group.id not in member.privileged_groups:
                message = (
                    f"privileged group {group.id} includes user {member.id}, "
                    "but the user does not list that privileged group"
                )
                raise ValueError(message)
