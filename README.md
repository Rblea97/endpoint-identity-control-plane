# Endpoint Identity Control Plane

A portfolio-grade FastAPI lab for endpoint and identity risk scoring using synthetic data.

**Status:** Local/demo portfolio project. Uses fake data only; not connected to real Microsoft tenants, Active Directory, SCCM/MECM, Intune, Entra ID, or Defender.

## Why this project exists

Endpoint Identity Control Plane is designed as a practical bridge from entry-level IT work into endpoint administration, identity administration, and endpoint/identity security engineering.

The project models the kinds of operational questions that appear in Microsoft-centered environments:

- Which endpoints are stale, noncompliant, or missing important security controls?
- Which users or groups create identity hygiene risk?
- Which device/user combinations should an IT or security team review first?
- What remediation steps should be prioritized?

All examples use synthetic demo data so the project can be safely reviewed, tested, and eventually published.

## What it demonstrates

- Endpoint inventory and lifecycle concepts.
- Identity hygiene and privileged-account review concepts.
- Deterministic risk scoring with evidence and remediation guidance.
- FastAPI service design with tests, type checking, linting, security scans, and CI.
- Public-project discipline: threat model, ADRs, runbooks, docs, and release gates.

## Current capabilities

Implemented now:

- FastAPI application scaffold.
- `GET /health` service health check.
- Local validation gates inherited from the secure Python service template.

Planned MVP capabilities:

- `GET /version` project metadata endpoint.
- Synthetic users, devices, and groups.
- Endpoint and identity risk findings.
- Prioritized risk report.
- Runbooks for common endpoint/identity review workflows.

## Safety boundaries

This project must not include:

- employer data;
- real user, device, hostname, group, or tenant exports;
- real Active Directory, SCCM/MECM, Intune, Entra ID, Defender, or Microsoft Graph data;
- secrets, API keys, credentials, or private screenshots;
- claims that the project is production-ready.

The intended data classification is:

> `synthetic-demo-data-only`

## Quick start

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
make all
uvicorn endpoint_identity_control_plane.app:app --reload
```

Open locally:

- API docs: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/health>

## Local container lane

This repository includes a local-only container rehearsal for the FastAPI app. It is intended for private sandbox validation, not production deployment or registry publication.

Build and inspect the image:

```bash
docker compose build api
docker compose config
```

Run the API on loopback only:

```bash
docker compose up -d api
curl --fail --silent http://127.0.0.1:8000/health
docker compose exec -T api id
docker compose down
```

## Development commands

```bash
make lint
make format-check
make typecheck
make test
make security
make all
```

`make security` runs advisory local checks. Public release requires the stricter public-release gate and file hygiene review.

## Project roadmap

1. **Scaffold hardening and project identity** — rename template artifacts and establish public-safe project purpose.
2. **Data model and synthetic fixtures** — add validated users, devices, and groups.
3. **Risk engine MVP** — implement deterministic endpoint and identity hygiene checks.
4. **API endpoints** — expose inventory, findings, and risk-report endpoints.
5. **Documentation foundation** — add architecture, threat model, ADRs, runbooks, and portfolio narrative.
6. **Public-readiness pass** — file hygiene audit, diagram rendering, final docs review, and scan finding classification.

Dashboard and live demo deployment are intentionally deferred until the working local system is complete and validated.

## Documentation

Key docs and planning artifacts:

- Design spec: `.hermes/plans/2026-05-22-endpoint-identity-control-plane-design-spec.md`
- Development guide: `AGENTS.md`
- Security policy: `SECURITY.md`
- Architecture docs: `docs/architecture.md`
- Threat model: `docs/threat-model.md`
- Security posture: `docs/security-posture.md`
- ADRs: `docs/adr/`

## Honest limitations

- This is not connected to a real Microsoft tenant.
- Findings are simplified and rule-based.
- The project is not a replacement for Microsoft Defender, Intune, Entra ID, SCCM/MECM, SIEM, or vulnerability management tooling.
- The first public version is intended to demonstrate engineering discipline and endpoint/identity security reasoning, not enterprise production readiness.
