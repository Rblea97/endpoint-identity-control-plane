# Threat Model

## Scope

This threat model covers the current local/demo FastAPI MVP:

- committed synthetic endpoint and identity inventory;
- FastAPI read-only endpoints;
- deterministic risk engine;
- local developer and CI validation workflow;
- documentation intended for eventual public review.

It does not cover a production deployment, real Microsoft tenant integration, write APIs, authentication, persistence, or VM-based lab infrastructure because those are not implemented yet.

## Assets

- Application source code.
- Synthetic demo inventory fixture.
- API responses and generated OpenAPI schema.
- Tests and validation evidence.
- Documentation, ADRs, and public-facing project narrative.
- CI/CD configuration and local developer tooling.

## Data classification

All committed demo inventory and API sample output must remain:

```text
synthetic-demo-data-only
```

Real employer, tenant, user, device, hostname, group, screenshot, credential, log, ticket, or export data is out of scope and must not be committed.

## Trust boundaries

### Local API client to FastAPI app

The API client is outside the application boundary. In the current MVP, clients can only call read-only `GET` endpoints. Future write or import endpoints would require stronger validation and authentication decisions.

### Repository fixture to application runtime

The committed JSON fixture is trusted only after validation. The loader and Pydantic models verify the shape and relationships before the app returns inventory or risk output.

### Source repository to public audience

The repo itself is a trust boundary because documentation, fixtures, plans, and checklists may eventually be public. File hygiene matters even if runtime behavior is safe.

### Local toolchain and dependency boundary

The project relies on Python packages, linters, scanners, and CI tooling. Dependency compromise or stale tooling could affect validation quality.

## Threats and current controls

### Real or sensitive data exposure

Risk: real employee, tenant, device, hostname, export, screenshot, credential, or employer-specific data is accidentally committed.

Current controls:

- Synthetic-only project scope documented in README, AGENTS, API docs, security posture, and ADRs.
- Demo usernames use fake `.example`-style values and hostnames use `DEMO-` prefixes.
- `data_classification` is present in inventory and report output.
- Gitleaks runs in the local security gate.

Residual risk:

- Secret scanning does not prove all sensitive business context is absent. Lane 6 must perform deliberate file hygiene review before publication.

### Stale or misleading public claims

Risk: docs imply production readiness, live Microsoft integration, or VM/domain functionality that does not exist.

Current controls:

- README and docs state local/demo scope and deferred controls.
- ADRs distinguish implemented decisions from future production controls.
- Lane validation checklists record what was actually tested.

Residual risk:

- Future changes can create docs drift. README, architecture, API, and ADRs must be reviewed during each maturity lane.

### Invalid synthetic inventory relationships

Risk: fixtures reference missing users, devices, or groups and produce misleading risk output.

Current controls:

- Pydantic inventory model validates relationships.
- Tests cover fixture loading and invalid references.

Residual risk:

- Business logic is simplified. The model is not a full replacement for enterprise CMDB, AD, SCCM/MECM, Intune, or Entra ID schema validation.

### Dependency and toolchain compromise

Risk: vulnerable or malicious dependencies affect runtime or validation.

Current controls:

- Minimal dependency footprint.
- `make all` includes pip-audit advisory checks.
- CI/dependency tooling is present in the baseline.

Residual risk:

- `pip-audit` cannot audit the local editable package as a PyPI dependency. That advisory note is expected and must be classified during release review.

### Unauthenticated access

Risk: if deployed publicly, anyone could read the demo endpoints.

Current controls:

- Project is documented as local/demo only.
- No secrets or real data are served.
- Live deployment is deferred.

Residual risk:

- Before any public hosted demo, add an explicit deployment threat model and decide whether demo authentication, rate limiting, request logging, and abuse controls are needed.

### Unsafe future integrations

Risk: future Microsoft Graph, AD, SCCM/MECM, Intune, Defender, or SIEM integrations could introduce credentials, real data, or excessive permissions.

Current controls:

- Real integrations are out of scope for the MVP.
- ADR-0004 documents the deferral.

Residual risk:

- Any future integration must be designed as a separate lane with least privilege, redaction, test fixtures, and no real-data publication.

## Residual risk summary

The current local MVP has low runtime sensitivity because it is read-only and synthetic-only. The main risks are publication hygiene, misleading claims, future scope creep, and dependency/tooling drift. These are addressed through docs, validation gates, and a planned public-readiness/file hygiene lane.
