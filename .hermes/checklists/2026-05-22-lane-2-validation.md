# Lane 2 Validation — Synthetic Inventory Models and Fixtures

Date: 2026-05-22
Project: Endpoint Identity Control Plane
Path: `/root/projects/endpoint-identity-control-plane`

## Scope validated

Lane 2 added the data foundation for the endpoint/identity lab:

- Pydantic models for users, devices, groups, and an inventory container.
- Strict model behavior with forbidden extra fields and frozen models.
- Cross-reference validation between users, devices, and privileged groups.
- Committed synthetic demo inventory fixture packaged with the application.
- Demo fixture loader with basic secret-marker rejection.
- Behavior tests for fixture loading, relationship consistency, fake-data conventions, and invalid references.

No risk findings, inventory API endpoints, dashboard, persistence, or external Microsoft integrations were added in this lane.

## Validation commands run

Using external virtualenv:

```bash
. /tmp/endpoint-identity-control-plane-venv/bin/activate
make all
```

Expanded checks:

```bash
python3 -m ruff check src tests
python3 -m ruff check src --select D,ANN,N,PL,ARG,SIM,C4,RET,TRY --preview
python3 -m ruff format --check src tests
python3 -m mypy src tests
python3 -m pytest tests -q
gitleaks detect --source . --no-git --redact
python3 -m bandit -q -r src
python3 -m pip_audit
```

## Results

- Ruff lint: passed.
- Strict source lint preview: passed.
- Ruff format check: passed — 7 files already formatted.
- mypy: passed — no issues in 7 source files.
- pytest: passed — `13 passed`.
- gitleaks: passed — no leaks found.
- bandit: passed.
- pip-audit: no known third-party vulnerabilities found.

## Findings and classification

- `endpoint-identity-control-plane Dependency not found on PyPI and could not be audited: endpoint-identity-control-plane (0.1.0)`
  - Classification: environment/tooling-only informational note.
  - Reason: expected for the local editable project package; not a third-party dependency vulnerability.

## Review notes

Codex initially changed the health/version tests to call route functions directly instead of exercising the FastAPI app. Hermes rejected that as HTTP-test drift and restored behavior-level `TestClient` tests before validation.

## Residual risks

- Fake-data safety checks are lightweight guardrails, not a full DLP solution.
- The demo fixture uses simplified synthetic relationships and should not be described as an enterprise import format.
- Risk rules are not implemented yet; this lane only provides validated inventory data for later rules.
