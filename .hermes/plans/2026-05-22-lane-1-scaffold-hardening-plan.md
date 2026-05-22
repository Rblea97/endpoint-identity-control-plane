# Lane 1 Scaffold Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the secure Python service scaffold into the named Endpoint Identity Control Plane project without adding risk-engine behavior yet.

**Architecture:** Keep the existing FastAPI template and public-readiness infrastructure. Update project identity, service metadata, health/version endpoints, tests, and documentation so later implementation lanes have a clean source of truth.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, pytest, Ruff, mypy, Bandit, pip-audit, GitHub Actions, Docker/Compose local lane.

---

## File structure for Lane 1

- Modify `AGENTS.md`: replace template placeholder with project-specific purpose and safety boundaries.
- Modify `README.md`: replace template README with project-specific public-facing overview and quick start.
- Modify `src/endpoint_identity_control_plane/app.py`: update app title and add `GET /version`.
- Modify `tests/test_health.py`: keep health test and add behavior-level version endpoint test.
- Keep `.hermes/plans/2026-05-22-endpoint-identity-control-plane-design-spec.md`: design source of truth.
- Run validation with the repo's Makefile.

## Task 1: Project identity docs

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

- [ ] **Step 1: Update `AGENTS.md` project purpose**

Replace the placeholder project purpose with:

```markdown
## Project purpose

Endpoint Identity Control Plane is a public portfolio FastAPI lab for practicing endpoint and identity security operations with synthetic data. It models users, groups, Windows endpoints, compliance state, lifecycle state, and risk findings inspired by SCCM/MECM, Active Directory, Intune, Entra ID, and Defender-style workflows.

The project is intended for local/demo use, hiring-manager review, and technical interview discussion. It must never include employer data, real tenant exports, real Active Directory/SCCM/Intune data, secrets, private screenshots, or production claims that the code does not support.
```

- [ ] **Step 2: Rewrite README for the actual project**

The README should include:

```markdown
# Endpoint Identity Control Plane

A portfolio-grade FastAPI lab for endpoint and identity risk scoring using synthetic data.

**Status:** Local/demo portfolio project. Uses fake data only; not connected to real Microsoft tenants, Active Directory, SCCM/MECM, Intune, Entra ID, or Defender.

## What it demonstrates

- Endpoint inventory and lifecycle concepts.
- Identity hygiene and privileged-account review concepts.
- Deterministic risk scoring with evidence and remediation guidance.
- FastAPI service design with tests, type checking, linting, security scans, and CI.
- Public-project discipline: threat model, ADRs, runbooks, docs, and release gates.
```

Also include quick start commands:

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
make all
uvicorn endpoint_identity_control_plane.app:app --reload
```

- [ ] **Step 3: Commit docs identity update**

```bash
git add AGENTS.md README.md .hermes/plans/2026-05-22-endpoint-identity-control-plane-design-spec.md .hermes/plans/2026-05-22-lane-1-scaffold-hardening-plan.md
git commit -m "docs: define endpoint identity control plane scope"
```

Expected: commit succeeds.

## Task 2: FastAPI service metadata

**Files:**
- Modify: `src/endpoint_identity_control_plane/app.py`
- Modify: `tests/test_health.py`

- [ ] **Step 1: Write/confirm test for health endpoint**

Expected test content:

```python
def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Run:

```bash
python -m pytest tests/test_health.py::test_health_returns_ok -q
```

Expected: pass.

- [ ] **Step 2: Add failing version endpoint test**

Add to `tests/test_health.py`:

```python
def test_version_returns_project_metadata() -> None:
    client = TestClient(app)
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "endpoint-identity-control-plane",
        "version": "0.1.0",
        "data_classification": "synthetic-demo-data-only",
    }
```

Run:

```bash
python -m pytest tests/test_health.py::test_version_returns_project_metadata -q
```

Expected: fail with `404 Not Found` before implementation.

- [ ] **Step 3: Implement app metadata and version endpoint**

Replace `src/endpoint_identity_control_plane/app.py` with:

```python
"""FastAPI application for Endpoint Identity Control Plane."""

from fastapi import FastAPI

APP_NAME = "endpoint-identity-control-plane"
APP_VERSION = "0.1.0"
DATA_CLASSIFICATION = "synthetic-demo-data-only"

app = FastAPI(
    title="Endpoint Identity Control Plane",
    summary="Endpoint and identity risk-scoring lab using synthetic data.",
    version=APP_VERSION,
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal health response for local and CI smoke checks."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    """Return project metadata for smoke tests and demo documentation."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "data_classification": DATA_CLASSIFICATION,
    }
```

- [ ] **Step 4: Run focused tests**

```bash
python -m pytest tests/test_health.py -q
```

Expected: both tests pass.

- [ ] **Step 5: Run formatting and type checks**

```bash
python -m ruff format --check src tests
python -m ruff check src tests
python -m mypy src tests
```

Expected: all pass.

- [ ] **Step 6: Commit metadata endpoint**

```bash
git add src/endpoint_identity_control_plane/app.py tests/test_health.py
git commit -m "feat: expose project version metadata"
```

Expected: commit succeeds.

## Task 3: Baseline validation

**Files:**
- No code changes expected unless validation exposes template drift.

- [ ] **Step 1: Install dependencies in an external virtualenv**

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

Expected: installation succeeds.

- [ ] **Step 2: Run full gate**

```bash
make all
```

Expected: pass, or any failures are classified as fixed, environment/tooling-only, false positive, accepted risk, or deferred.

- [ ] **Step 3: Record validation result**

Create or update `.hermes/checklists/2026-05-22-lane-1-validation.md` with commands run, results, findings, and residual risk.

- [ ] **Step 4: Commit validation note**

```bash
git add .hermes/checklists/2026-05-22-lane-1-validation.md
git commit -m "docs: record lane 1 validation"
```

Expected: commit succeeds.

## Self-review

Spec coverage:

- Covers scaffold hardening and project identity from Lane 1.
- Does not implement data models, risk engine, inventory APIs, or docs polish lanes; those are later lanes.

Placeholder scan:

- No `TBD`, `TODO`, or unresolved placeholders are intentionally present in the implementation steps.

Type consistency:

- `APP_NAME`, `APP_VERSION`, and `DATA_CLASSIFICATION` are all `str`.
- `/version` response shape matches the test exactly.
