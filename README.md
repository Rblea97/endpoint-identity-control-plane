# Endpoint Identity Control Plane

A local FastAPI lab that models endpoint and identity risk using synthetic Windows/identity inventory data.

**Status:** Portfolio/demo project for local review. It uses fake data only and does not connect to real Microsoft tenants, Active Directory, SCCM/MECM, Intune, Entra ID, Defender, or employer systems.

## Overview

Endpoint Identity Control Plane is designed as a practical bridge from entry-level IT work into endpoint administration, identity administration, and endpoint security. It models common review questions from Microsoft-centered IT environments without requiring a live domain, real tenant, or virtual machine lab.

The current backend loads committed synthetic inventory, validates it with Pydantic models, evaluates deterministic endpoint/identity risk rules, and exposes the results through a small FastAPI API. The goal is to show clean engineering and realistic operational reasoning, not to imitate enterprise tooling or process real company data.

The data classification for all committed examples and API responses is:

```text
synthetic-demo-data-only
```

## What it demonstrates

- Endpoint inventory concepts: hostname, OS baseline, patch status, encryption, local admin exposure, compliance state, imaging state, and check-in freshness.
- Identity concepts: users, groups, privileged-group membership, MFA status, disabled accounts, stale logins, and device assignment.
- Deterministic risk scoring with evidence, severity, category, remediation guidance, and control mappings.
- FastAPI service design with typed response models and generated OpenAPI docs.
- Public-safe software discipline: synthetic fixtures, tests, type checking, linting, security scans, ADRs, threat model, and validation checklists.

## Quick start

```bash
git clone <repo-url>
cd endpoint-identity-control-plane
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
make all
uvicorn endpoint_identity_control_plane.app:app --reload
```

Open locally:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/health>
- Risk report: <http://127.0.0.1:8000/risk-report>

## Example request

```bash
curl --silent http://127.0.0.1:8000/risk-report
```

Shortened example response:

```json
{
  "generated_at": "2026-05-22T12:00:00Z",
  "data_classification": "synthetic-demo-data-only",
  "finding_counts_by_severity": {
    "high": 9,
    "medium": 4
  },
  "finding_counts_by_category": {
    "lifecycle": 1,
    "imaging": 2,
    "identity": 2,
    "endpoint": 5,
    "compliance": 3
  },
  "top_risky_assets": [
    {
      "asset_type": "device",
      "asset_id": "device-003",
      "finding_count": 6,
      "highest_severity": "high"
    }
  ]
}
```

## Implemented API endpoints

- `GET /health` — local and CI smoke check.
- `GET /version` — app name, version, and data classification.
- `GET /users` — synthetic identity records.
- `GET /devices` — synthetic endpoint records.
- `GET /groups` — synthetic group records.
- `GET /findings` — deterministic endpoint and identity findings.
- `GET /risk-report` — summarized risk report with counts and top risky assets.

See `docs/api.md` for endpoint examples and response notes.

## Current risk rules

The v1 rule engine flags conditions such as:

- privileged user without MFA;
- disabled user still assigned to a device;
- stale user login beyond the demo threshold;
- stale endpoint check-in beyond the demo threshold;
- Windows 10 treated as an unsupported baseline for the demo timeline;
- disk encryption disabled;
- excessive local administrator exposure;
- noncompliant endpoint state;
- failed or in-progress imaging state;
- missing or unknown patch status.

The rule engine is deterministic on purpose. It is easier to test, explain, and review than an ML/LLM-based scoring system for this stage of the project.

## Architecture

At this stage the service is intentionally small:

```text
API client
  -> FastAPI route
  -> synthetic inventory loader
  -> Pydantic models
  -> deterministic risk engine
  -> JSON response
```

There is no database, authentication layer, live Microsoft integration, or VM dependency in the current MVP.

Deeper docs:

- Architecture: `docs/architecture.md`
- API: `docs/api.md`
- Threat model: `docs/threat-model.md`
- Security posture: `docs/security-posture.md`
- ADRs: `docs/adr/`
- Portfolio narrative: `docs/portfolio-narrative.md`

## Validation commands

```bash
make lint
make lint-src-strict
make format-check
make typecheck
make test
make security
make all
```

`make all` runs linting, strict source linting, formatting check, mypy, pytest, and advisory security checks. Public release still requires a separate file-hygiene and publication-readiness pass.

## Local container lane

This repository includes a local-only container rehearsal for the FastAPI app. It is intended for private sandbox validation, not production deployment or registry publication.

```bash
docker compose build api
docker compose config
docker compose up -d api
curl --fail --silent http://127.0.0.1:8000/health
docker compose down
```

## Roadmap

Completed:

1. Scaffold hardening and project identity.
2. Synthetic data models and fixture loader.
3. Deterministic endpoint/identity risk engine.
4. Inventory, findings, and risk-report API endpoints.
5. Public documentation foundation.

Next:

6. Public-readiness/file hygiene pass.
7. Optional dashboard or static UI.
8. Optional live demo deployment after the local system and docs are stable.

## Scope and limitations

- This is not connected to a real Microsoft tenant, domain, SCCM/MECM site, Intune tenant, Entra ID tenant, Defender portal, SIEM, or vulnerability scanner.
- This project does not require virtual machines for the main demo.
- The inventory is committed synthetic JSON, not an import from a live system.
- The risk rules are simplified and deterministic.
- There is no authentication, persistence, multi-tenant model, or production deployment in the current MVP.
- The project is not a replacement for Microsoft Defender, Intune, Entra ID, SCCM/MECM, SIEM, asset management, or vulnerability management tooling.

## Data safety

Do not add real employer, tenant, user, device, hostname, group, screenshot, credential, log, or export data. Use only synthetic examples that are safe for public review.
