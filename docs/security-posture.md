# Security Posture

## Scope

This document describes the security posture of the current local/demo MVP. The project is a portfolio lab that uses committed synthetic inventory and read-only FastAPI endpoints.

The current scope protects against:

- committing secrets or real tenant/employer data;
- serving misleading or unvalidated synthetic inventory;
- accepting unreviewed AI-generated code without tests and scans;
- publishing stale claims without a documented review path.

Out of scope for the current MVP:

- production deployment;
- authentication and authorization;
- persistence/database security;
- Microsoft Graph, AD, SCCM/MECM, Intune, Entra ID, Defender, or SIEM integration;
- real endpoint telemetry;
- VM lab infrastructure.

## Security goals

- Keep all committed examples public-safe and synthetic.
- Validate inventory structure and relationships before generating risk output.
- Keep runtime behavior deterministic and testable.
- Make validation repeatable with linting, typing, tests, and security scans.
- Document implemented controls separately from deferred production controls.

## Implemented controls

### Data safety

- Inventory fixture is committed synthetic JSON.
- API metadata and risk reports use `synthetic-demo-data-only` classification.
- README, AGENTS, API docs, threat model, and ADRs prohibit real employer/tenant data.
- Demo usernames, hostnames, departments, and group names are fake.

### Validation

- Pydantic models validate users, devices, groups, and inventory references.
- Risk findings and risk reports are typed Pydantic models with `extra="forbid"` and frozen behavior.
- Tests cover fixture loading, relationship validation, API routes, risk findings, and report summaries.

### Application behavior

- Current API endpoints are read-only.
- There are no write endpoints, credentials, sessions, cookies, or external integrations.
- Demo risk report timestamp is deterministic so examples and tests do not drift.

### Development and review gates

`make all` runs:

- Ruff linting;
- strict Ruff source checks;
- Ruff format check;
- mypy;
- pytest;
- Gitleaks advisory scan;
- Bandit;
- pip-audit advisory scan.

### Repository governance

- `.hermes/plans/` stores durable specs and lane plans.
- `.hermes/checklists/` stores validation results.
- `AGENTS.md` defines coding, security, and public-safety expectations.
- ADRs record major architecture decisions and deferred controls.

## Known limitations

- No authentication or authorization.
- No rate limiting.
- No production logging, monitoring, tracing, or alerting.
- No database or persistence controls.
- No live integrations with Microsoft or enterprise systems.
- No live deployment hardening.
- No VM lab or domain controller.
- Secret scanning cannot prove that all business-sensitive context is absent; a file hygiene lane is still required before publication.

## Finding classification standard

Security or validation findings must be classified as one of:

- **Fixed:** code/docs/config changed and validation re-ran.
- **Accepted risk:** real risk remains with a written justification.
- **False positive:** finding is not applicable, with evidence.
- **Environment/tooling-only issue:** caused by local tooling or scanner limitations, not project risk.
- **Deferred:** valid issue intentionally moved to a later lane with a named follow-up.

Current known advisory note:

- `pip-audit` may report that the local editable package `endpoint-identity-control-plane` is not found on PyPI and cannot be audited. Classification: environment/tooling-only advisory for the local package itself. Third-party dependency findings still require triage.

## Before public release

Complete Lane 6 public-readiness/file hygiene review before publishing:

- inventory tracked files;
- scan suspicious filenames and content;
- verify `.gitignore` and `.dockerignore` coverage;
- classify `.hermes` artifacts as curated evidence or private scratch;
- rerun full validation;
- classify all scanner findings;
- ensure docs make no unsupported production or integration claims.
