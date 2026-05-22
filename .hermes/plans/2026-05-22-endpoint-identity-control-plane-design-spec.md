# Endpoint Identity Control Plane — Design Spec

Date: 2026-05-22
Status: Draft approved for implementation planning
Project path: `/root/projects/endpoint-identity-control-plane`

## 1. Purpose

Endpoint Identity Control Plane is a public portfolio project that demonstrates how entry-level endpoint operations experience can grow into endpoint administration, identity administration, and endpoint/identity security engineering.

The project is a local/demo FastAPI service that ingests or ships with synthetic endpoint and identity inventory data, evaluates operational and security hygiene rules, and produces prioritized findings with evidence and remediation guidance.

The project must be credible to hiring managers and recruiters in roughly a 60-second GitHub skim while still standing up to deeper technical review through tests, documentation, threat modeling, ADRs, and repeatable validation.

## 2. Career narrative

The project supports this narrative:

> I started with enterprise IT work around Windows endpoints, imaging, SCCM/MECM concepts, and Active Directory. I built this lab to practice moving from support tasks into endpoint and identity security: inventory, compliance, stale object review, privileged identity hygiene, local admin risk, and remediation prioritization.

Target next-role signals:

- Endpoint Administrator
- Desktop Engineer
- Junior Systems Administrator
- SCCM/MECM or Intune Administrator
- IAM Analyst
- Endpoint Security Analyst
- Microsoft 365 / Entra administrator track

## 3. Non-goals and safety boundaries

The project must not:

- use employer data, tenant exports, AD dumps, SCCM data, Intune data, logs, screenshots, hostnames, usernames, or policy names from a real workplace;
- connect to real Microsoft Graph, AD, SCCM/MECM, Intune, Defender, or Entra APIs in v1;
- claim production readiness or enterprise integration in v1;
- store or require secrets in the repository;
- log sensitive request bodies or arbitrary headers;
- implement offensive security behavior.

Allowed data is synthetic demo data only.

## 4. Recommended architecture

Use the existing secure Python/FastAPI template as the infrastructure baseline.

Architecture style:

- FastAPI backend first.
- Pure-Python risk engine separated from HTTP route handlers.
- Static synthetic JSON fixtures for v1 data.
- Pydantic schemas at the API boundary.
- Deterministic scoring and findings for testability.
- CLI/reporting and dashboard deferred until after the API/risk engine is stable.

Initial package name: `endpoint_identity_control_plane`.

## 5. MVP capabilities

### 5.1 Health and metadata

Endpoints:

- `GET /health`
- `GET /version`

Purpose:

- prove service startup;
- expose stable app metadata for smoke tests and demo docs.

### 5.2 Synthetic inventory APIs

Endpoints:

- `GET /users`
- `GET /devices`
- `GET /groups`

Data source:

- committed synthetic JSON files under `data/demo/` or package resources.

User fields, v1:

- `id`
- `username`
- `display_name`
- `department`
- `enabled`
- `last_login_at`
- `mfa_enabled`
- `privileged_groups`
- `assigned_device_ids`

Device fields, v1:

- `id`
- `hostname`
- `assigned_user_id`
- `os_name`
- `os_version`
- `last_checkin_at`
- `patch_status`
- `encryption_enabled`
- `local_admin_count`
- `compliance_state`
- `imaging_state`

Group fields, v1:

- `id`
- `name`
- `privilege_level`
- `member_user_ids`

### 5.3 Risk findings

Endpoints:

- `GET /findings`
- `GET /risk-report`

Finding fields:

- `id`
- `severity`: `low`, `medium`, `high`, `critical`
- `category`: `identity`, `endpoint`, `compliance`, `lifecycle`, `imaging`
- `title`
- `asset_type`: `user`, `device`, `group`
- `asset_id`
- `evidence`
- `recommendation`
- `control_mapping`

Initial checks:

1. privileged user without MFA;
2. disabled/inactive user still assigned to active device;
3. stale user login beyond configured threshold;
4. stale device check-in beyond configured threshold;
5. unsupported or outdated OS version;
6. endpoint encryption disabled;
7. excessive local administrator exposure;
8. noncompliant endpoint;
9. failed or incomplete imaging state;
10. missing/unknown patch status.

### 5.4 Risk report

The risk report should summarize:

- finding counts by severity;
- finding counts by category;
- top risky users;
- top risky devices;
- highest-priority remediation actions;
- generated timestamp;
- clear note that all data is synthetic.

## 6. Public documentation requirements

The repository should eventually include:

- README optimized for 60-second hiring-manager skim;
- quick-start instructions;
- example API output;
- architecture doc;
- data model doc;
- threat model;
- security posture doc;
- ADR index and project-specific ADRs;
- testing doc;
- runbooks;
- portfolio narrative;
- high-contrast Mermaid diagrams rendered to assets before public release.

Initial runbooks:

- investigate stale endpoint;
- review privileged account missing MFA;
- triage noncompliant endpoint;
- review device assigned to inactive user;
- handle failed imaging/deployment state.

## 7. Testing and quality gates

Required local commands before accepting implementation lanes:

```bash
make lint
make typecheck
make test
make security
make all
```

Test requirements:

- risk rules must be unit tested with focused synthetic fixtures;
- API endpoints must be tested through FastAPI `TestClient` or equivalent behavior-level tests;
- tests must prove both normal output and edge cases;
- no tests should rely on current date without controlling time;
- security-sensitive behavior must include no-real-data/no-secret expectations where applicable.

## 8. Security posture

Initial security posture:

- local/demo-only app;
- no auth in v1 unless a later lane explicitly adds local/demo API-key auth;
- no external integrations;
- no real tenant or employer data;
- bounded synthetic input;
- no secrets required;
- no arbitrary shell execution;
- least-privilege CI permissions inherited from template;
- dependency scanning and secret scanning through existing template gates.

Residual risks:

- v1 does not prove real Microsoft tenant integration;
- v1 findings are rule-based and simplified;
- v1 should not be presented as a production endpoint security platform;
- public release requires a file hygiene audit and docs polish lane before publishing.

## 9. Implementation lanes

### Lane 1 — Scaffold hardening and project identity

Goals:

- keep the secure template baseline;
- replace placeholder naming;
- update project purpose in `AGENTS.md`, README, and package metadata;
- add durable spec and planning files;
- run baseline validation.

### Lane 2 — Data model and synthetic fixtures

Goals:

- add Pydantic/domain models;
- add synthetic demo users, devices, and groups;
- add fixture loader with validation;
- add tests proving fixture validity.

### Lane 3 — Risk engine MVP

Goals:

- implement deterministic rule checks;
- produce findings with evidence and remediation;
- add unit tests for every rule.

### Lane 4 — API endpoints

Goals:

- expose inventory, findings, and risk-report endpoints;
- test endpoints through behavior-level HTTP tests;
- update OpenAPI/API docs.

### Lane 5 — Public documentation foundation

Goals:

- rewrite README for the actual project;
- update architecture, threat model, security posture, and portfolio narrative;
- add initial runbooks.

### Lane 6 — Public-readiness pass

Goals:

- run file hygiene audit;
- render diagrams;
- validate links/docs;
- classify scan findings;
- prepare for GitHub publication.

Dashboard and live demo are deferred until after the working system is stable.

## 10. Acceptance criteria for MVP

The MVP is complete when:

- the app starts locally;
- health/version endpoints work;
- synthetic inventory endpoints return validated demo data;
- findings and risk report are deterministic;
- all initial risk checks are covered by meaningful tests;
- README explains what the project is, why it exists, what it demonstrates, and how to run it;
- docs clearly state synthetic data only;
- `make all` passes or any failures are classified;
- no secrets, real employer data, or misleading production claims are present.

## 11. Open decisions

Resolved:

- Start with FastAPI backend + risk engine first.
- Use synthetic data only.
- Defer dashboard and live demo.
- Treat this as a public portfolio project, but do not publish until public-readiness gates pass.

Open for later:

- whether to add a CLI report command;
- whether to add local/demo API-key auth;
- whether to add SQLite persistence;
- whether the dashboard should be React, static HTML, or generated report;
- where to deploy the live demo once the local system is mature.
