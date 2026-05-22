# Lane 3 Validation — Deterministic Risk Engine MVP

Date: 2026-05-22
Project: Endpoint Identity Control Plane
Path: `/root/projects/endpoint-identity-control-plane`

## Scope validated

Lane 3 added pure-Python endpoint and identity risk evaluation over validated synthetic inventory.

Implemented:

- `Finding`, `AssetRiskSummary`, and `RiskReport` Pydantic models.
- Deterministic `evaluate_inventory()` function using a caller-provided `as_of` timestamp.
- Deterministic `build_risk_report()` summary with severity counts, category counts, top risky assets, and findings.
- V1 checks for privileged user without MFA, disabled user with assigned device, stale user login, stale device check-in, Windows 10 demo unsupported baseline, encryption disabled, local admin exposure, noncompliant endpoint, incomplete/failed imaging, and missing/unknown patch status.
- Behavior tests for expected demo findings, finding fields, report summaries, top risky asset selection, and deterministic output.

Not implemented in this lane:

- FastAPI inventory/findings/report endpoints.
- Dashboard or live demo.
- Persistence.
- Real Microsoft integrations.

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
- Ruff format check: passed — 9 files already formatted.
- mypy: passed — no issues in 9 source files.
- pytest: passed — `18 passed`.
- gitleaks: passed — no leaks found.
- bandit: passed.
- pip-audit: no known third-party vulnerabilities found.

## Findings and classification

- `endpoint-identity-control-plane Dependency not found on PyPI and could not be audited: endpoint-identity-control-plane (0.1.0)`
  - Classification: environment/tooling-only informational note.
  - Reason: expected for the local editable project package; not a third-party dependency vulnerability.

## Residual risks

- The risk engine is rule-based and intentionally simplified for portfolio/demo use.
- Windows 10 is treated as unsupported in this demo timeline; this should be documented before public release.
- The risk engine has no HTTP surface yet; API exposure comes in Lane 4.
- Risk scoring is currently finding-count/severity based; richer weighted scoring can be a later maturity lane.
