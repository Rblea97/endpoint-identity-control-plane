"""Static checks for container lane configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    """Read a repository file as UTF-8 text."""

    return (ROOT / relative_path).read_text(encoding="utf-8")


def active_dockerignore_lines() -> set[str]:
    """Return active, non-comment Docker ignore patterns."""

    lines = set()
    for line in read_text(".dockerignore").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.add(stripped)
    return lines


def dockerfile_instructions() -> list[tuple[str, str]]:
    """Return simple Dockerfile instructions, ignoring comments and blank lines."""

    instructions: list[tuple[str, str]] = []
    for line in read_text("Dockerfile").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or line.startswith((" ", "\t")):
            continue
        keyword, _, rest = stripped.partition(" ")
        instructions.append((keyword.upper(), rest.strip()))
    return instructions


def compose_config() -> dict[str, Any]:
    """Parse the committed Compose config."""

    parsed = yaml.safe_load(read_text("compose.yml"))
    assert isinstance(parsed, dict)
    return cast("dict[str, Any]", parsed)


def api_service() -> dict[str, Any]:
    """Return the Compose API service definition."""

    services = compose_config().get("services")
    assert isinstance(services, dict)
    service = services.get("api")
    assert isinstance(service, dict)
    return cast("dict[str, Any]", service)


def test_dockerfile_uses_non_root_runtime_user() -> None:
    """Dockerfile should create and finish as a non-root runtime user."""

    instructions = dockerfile_instructions()
    users = [rest for keyword, rest in instructions if keyword == "USER"]
    runs = [rest for keyword, rest in instructions if keyword == "RUN"]

    assert any("useradd" in run or "adduser" in run for run in runs)
    assert users, "Dockerfile must declare a runtime USER"
    assert users[-1] not in {"0", "root"}
    assert users[-1] == "appuser"


def test_dockerfile_runs_fastapi_app_on_expected_host_and_port() -> None:
    """Dockerfile command should run this app through Uvicorn on port 8000."""

    instructions = dockerfile_instructions()
    runtime_commands = [rest for keyword, rest in instructions if keyword in {"CMD", "ENTRYPOINT"}]

    assert runtime_commands, "Dockerfile must define CMD or ENTRYPOINT"
    final_command = runtime_commands[-1]
    assert "endpoint_identity_control_plane.app:app" in final_command
    assert "uvicorn" in final_command
    assert "0.0.0.0" in final_command  # noqa: S104 # nosec B104 - container internal bind.
    assert "8000" in final_command


def test_dockerignore_excludes_generated_and_sensitive_paths() -> None:
    """Docker build context should exclude generated files and sensitive inputs."""

    dockerignore = active_dockerignore_lines()
    required_patterns = {
        ".git",
        ".env",
        ".env.*",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "__pycache__",
        "*.egg-info",
        ".hermes/reports",
        "*.db",
        "*.sqlite",
        "*.sqlite3",
        "venv",
        ".venv",
        "id_rsa",
        "id_ed25519",
        "*.pem",
        "*.key",
    }

    assert required_patterns <= dockerignore


def test_compose_binds_api_to_localhost_only() -> None:
    """Compose should expose the API only on the loopback interface."""

    ports = api_service().get("ports")
    assert isinstance(ports, list)
    assert ports, "API service must publish a localhost development port"

    for port in ports:
        if isinstance(port, str):
            assert port.startswith("127.0.0.1:"), port
            assert not port.startswith(("0.0.0.0:", ":")), port
        elif isinstance(port, dict):
            assert port.get("host_ip") == "127.0.0.1", port
        else:
            raise AssertionError(f"Unexpected Compose port entry: {port!r}")


def test_compose_avoids_privileged_runtime_and_docker_socket_mounts() -> None:
    """Compose should avoid privileged containers and Docker socket mounts."""

    service = api_service()
    volumes = service.get("volumes", [])

    assert service.get("privileged") not in {True, "true", "True"}
    assert service.get("network_mode") != "host"
    assert all("/var/run/docker.sock" not in str(volume) for volume in volumes)


def test_compose_applies_local_hardening_controls() -> None:
    """Compose should apply local least-privilege hardening controls."""

    service = api_service()

    assert service.get("read_only") is True
    assert "ALL" in service.get("cap_drop", [])
    assert "no-new-privileges:true" in service.get("security_opt", [])
    assert "/tmp" in service.get("tmpfs", [])  # noqa: S108 # nosec B108 - verifies tmpfs.
