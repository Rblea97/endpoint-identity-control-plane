# Portfolio Narrative

Use this document to explain the project in interviews, portfolio reviews, and README-linked project discussions. Keep the explanation honest: this is a local synthetic-data lab, not production software and not a live employer integration.

## Short pitch

Endpoint Identity Control Plane is a FastAPI backend that models endpoint and identity hygiene using synthetic Windows/identity inventory. It loads fake users, devices, and groups, validates their relationships, runs deterministic risk rules, and exposes findings through API endpoints.

I built it to connect entry-level IT concepts such as SCCM/MECM imaging, Active Directory-style users and groups, endpoint compliance, patch status, local admin exposure, and stale devices to the next step: endpoint administration, identity administration, and endpoint security engineering.

## Why this is job-adjacent

The project is close to realistic IT operations without using real company data. It models questions an endpoint or identity team might ask:

- Which machines have stale check-ins?
- Which machines are noncompliant or missing important controls?
- Which users are disabled but still assigned to devices?
- Which privileged users need MFA review?
- Which devices should be reviewed first based on multiple findings?

This lines up with experience around imaging, endpoint lifecycle, Active Directory concepts, SCCM/MECM-style device management, and Microsoft-oriented security operations.

## What this project demonstrates

### Endpoint and identity reasoning

- User/device/group relationships.
- Endpoint lifecycle and imaging state.
- Patch and compliance status.
- Local administrator exposure.
- MFA and privileged-group review.
- Stale account and stale device hygiene.

### Backend engineering

- FastAPI route design.
- Pydantic models for structured data and validation.
- Deterministic service logic separated from API routing.
- Tests that exercise both pure Python logic and HTTP endpoints.
- Typed Python with mypy.

### DevSecOps and public-project discipline

- Synthetic-only data policy.
- Secret scanning with Gitleaks.
- Static security scanning with Bandit.
- Dependency advisory scan with pip-audit.
- Linting, formatting, and type-checking gates.
- Threat model, security posture, ADRs, and validation checklists.

## Why there are no VMs in the main project

The main project is an API/backend lab, not a domain-controller homelab. Virtual machines would make the project heavier, slower to reproduce, and harder for a reviewer to run.

The VM-free design is intentional:

- Recruiters and engineers can review the API and tests quickly.
- The project is safer to publish because it never needs real tenant or domain data.
- The synthetic data still maps to real endpoint/identity concepts.
- Optional VM or Microsoft integration labs can be added later as separate extensions.

## What I would say in an interview

A concise explanation:

> I wanted a project that connects directly to endpoint support and identity administration work, not a random cybersecurity demo. I built a FastAPI control-plane simulator that uses synthetic users, devices, and groups, validates the inventory, and runs deterministic rules for issues like privileged users without MFA, stale devices, local admin exposure, encryption gaps, compliance state, and imaging failures. The project is intentionally local and synthetic-only so it can be public and safe to review.

If asked why deterministic rules instead of AI/ML:

> I chose deterministic rules because the goal is explainability, testability, and operational clarity. For endpoint and identity hygiene, a reviewer should be able to see the evidence, the rule, the severity, and the remediation recommendation without guessing how a model reached the result.

If asked what I would add before production:

> I would add authentication, authorization, tenant separation, persistence, audit logging, rate limiting, secure ingestion, secrets management, observability, deployment hardening, and a stricter data governance model. I would also treat any Microsoft Graph or endpoint management integration as a separate least-privilege design.

## Honest limitations to mention

- It is a portfolio/demo backend, not production software.
- It uses synthetic fixture data, not real AD/SCCM/Intune/Entra/Defender data.
- It does not currently have a dashboard.
- It does not require or provision VMs.
- It does not include auth, persistence, or live deployment yet.
- Risk scoring is simplified and rule-based.

## Good resume bullet candidates

- Built a FastAPI endpoint and identity risk lab using synthetic Windows/identity inventory, Pydantic validation, deterministic risk rules, and typed JSON APIs.
- Modeled endpoint security hygiene checks including stale check-ins, patch status, encryption, local admin exposure, compliance state, imaging state, and privileged-user MFA review.
- Added portfolio-grade validation gates with pytest, Ruff, mypy, Bandit, Gitleaks, pip-audit, ADRs, threat model, and public-safe data handling documentation.

## Next portfolio improvements

- Public-readiness/file hygiene pass.
- Rendered architecture diagrams.
- Optional minimal dashboard for non-technical reviewers.
- Optional live hosted demo after local docs and safety gates are complete.
- Optional import simulator that accepts synthetic CSV/JSON exports shaped like endpoint-management reports.
