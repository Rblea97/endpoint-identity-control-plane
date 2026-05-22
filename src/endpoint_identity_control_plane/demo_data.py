"""Loader for committed synthetic demo inventory fixtures."""

from __future__ import annotations

import re
from pathlib import Path

from endpoint_identity_control_plane.models import Inventory

DEMO_INVENTORY_PATH = Path(__file__).parent / "data" / "demo" / "inventory.json"
UNSAFE_FIXTURE_MESSAGE = "fixture contains a secret-like marker"

_SECRET_LIKE_MARKERS = (
    re.compile(r"\bpassword\b", re.IGNORECASE),
    re.compile(r"\bsecret\b", re.IGNORECASE),
    re.compile(r"\btoken\b", re.IGNORECASE),
    re.compile(r"\btenant_id\b", re.IGNORECASE),
    re.compile(r"\bclient_secret\b", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----", re.IGNORECASE),
)


def load_demo_inventory(path: Path | None = None) -> Inventory:
    """Load and validate a synthetic demo inventory fixture."""
    fixture_path = path or DEMO_INVENTORY_PATH
    raw_fixture = fixture_path.read_text(encoding="utf-8")
    _reject_secret_like_markers(raw_fixture, fixture_path)
    return Inventory.model_validate_json(raw_fixture)


def _reject_secret_like_markers(raw_fixture: str, fixture_path: Path) -> None:
    for marker in _SECRET_LIKE_MARKERS:
        if marker.search(raw_fixture):
            message = f"{fixture_path} {UNSAFE_FIXTURE_MESSAGE}"
            raise ValueError(message)
