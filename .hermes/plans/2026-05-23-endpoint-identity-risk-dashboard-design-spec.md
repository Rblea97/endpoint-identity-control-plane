# Endpoint + Identity Risk Dashboard Design Spec

> **For Hermes:** This is the durable project source of truth for the next portfolio lane. Preserve the existing repository, use only synthetic data, and do not publish/deploy/push without Richie's explicit approval.

**Goal:** Extend Endpoint Identity Control Plane into a stronger recruiter-visible Endpoint + Identity Risk Dashboard that correlates endpoint state, identity ownership, patch/vulnerability priority, remediation workflow, and before/after risk reduction.

**Architecture:** Build on the current FastAPI + deterministic risk engine + CLI operations demo + static `site/` dashboard. Keep v1 local/static and synthetic. Add only the minimum model, scoring, exporter, UI, tests, and docs changes needed to make the dashboard visibly connect endpoint, identity, patch/compliance, and helpdesk remediation workflows.

**Tech Stack:** Python 3.11, FastAPI, Pydantic v2, pytest, Ruff, mypy, Bandit, pip-audit, vanilla HTML/CSS/JavaScript static dashboard.

---

## Current-state summary from repo inspection

Inspected repository: `/root/workspace/endpoint-identity-control-plane`

Git state at inspection:

- Branch: `main`
- Remote: `https://github.com/Rblea97/endpoint-identity-control-plane.git`
- Working tree: clean before this plan write
- Head: `db25c1734840c3ecef81181cb5a795f1b6863db94587`
- Latest commit: `feat: add clickable static UI demo (#4)`

Existing reusable assets:

- `AGENTS.md`: public-safe project instructions and quality gate expectations.
- `README.md`: strong 60-second project narrative, quick start, API list, risk rules, validation commands.
- `SECURITY.md`: basic secret handling and review expectations.
- `.hermes/plans/`: prior lane plans through Lane 8 clickable UI demo.
- `.hermes/checklists/`: validation logs and public-readiness checklists.
- `src/endpoint_identity_control_plane/models.py`: strict synthetic inventory models for users, devices, groups.
- `src/endpoint_identity_control_plane/risk.py`: deterministic rule engine and summarized risk report.
- `src/endpoint_identity_control_plane/operations_demo.py`: ticket-style CLI scenarios.
- `src/endpoint_identity_control_plane/data/demo/inventory.json`: committed synthetic fixture.
- `scripts/export_static_demo.py`: static JSON exporter for the browser demo.
- `site/index.html`, `site/styles.css`, `site/app.js`, `site/demo-data.json`: clickable static dashboard.
- `tests/`: API, fixture, risk, CLI/demo, static demo, and container tests.

Quick validation evidence at inspection:

- `make test` failed in the uninstalled shell because `endpoint_identity_control_plane` was not importable.
- `PYTHONPATH=src python3 -m pytest tests -q` passed: `34 passed in 0.46s`.
- `python3 scripts/export_static_demo.py` failed in the uninstalled shell for the same import-path reason.
- Conclusion: the code appears testable with `PYTHONPATH=src`, but full repo validation should use an external virtualenv and `python -m pip install -e '.[dev]'` before acceptance. Do not treat the raw `make test` failure as a code regression until the environment is installed.

Reusable direction:

- Keep deterministic scoring. It is explainable, testable, and interview-friendly.
- Keep the static dashboard. It is the best recruiter-visible surface.
- Extend existing data and scoring rather than introducing real integrations or a database.

Stale/risky areas:

- Current model has coarse `patch_status` only; it does not yet model vulnerability records, patch deadlines, or remediation status.
- Current dashboard shows risky devices and findings but not a true remediation queue, risk reduction, or owner-centric risk story.
- Current validation requires environment setup; final acceptance must run from an installed external venv.

Do not touch without explicit approval:

- GitHub Pages deployment settings beyond local/manual workflow changes.
- Repository visibility, remote settings, branch protection, or publishing.
- Real Microsoft, AD, SCCM/MECM, Intune, Entra, Defender, or ticketing integrations.
- Secrets, real tenant data, employer data, real hostnames, screenshots, usernames, tickets, or production-like identifiers.

## Scope

In scope for this lane:

1. Synthetic data expansion for patch/vulnerability/remediation signals.
2. Deterministic risk scoring enhancements that correlate endpoint state with identity owner context.
3. A dashboard view that makes the risk story obvious in under 60 seconds.
4. Ticket-style remediation queue and before/after risk reduction demo.
5. Tests for models, risk scoring, static exporter shape, and dashboard-required payload fields.
6. README/docs updates describing the dashboard, fake data, and demo workflow.
7. Final quality gate and findings classification.

Out of scope for v1:

- Real auth.
- Real Graph, Intune, Entra, AD, SCCM/MECM, Defender, vulnerability scanner, or ticketing integrations.
- Paid cloud resources.
- Public deployment or GitHub Pages publication.
- Production database/persistence unless already approved in a later lane.
- Complex RBAC, multi-tenancy, background jobs, or a broad rewrite.
- New repository creation.

## Data model design

Add minimal explicit models while preserving existing fields:

### Existing entities to preserve

- `User`
- `Device`
- `Group`
- `Inventory`

### New or expanded synthetic fields/entities

Recommended additions:

- `VulnerabilityRecord`
  - `id`: stable fake identifier such as `vuln-001`
  - `device_id`: references a known synthetic device
  - `title`: public-safe fake title, not a real internal finding
  - `severity`: `low | medium | high | critical`
  - `cvss_score`: bounded numeric demo score if useful
  - `status`: `open | remediated | accepted`
  - `discovered_at`: ISO timestamp
  - `patch_available`: boolean
  - `recommended_action`: remediation text

- `RemediationTicket`
  - `id`: stable fake ticket such as `ticket-001`
  - `asset_type`: `user | device | group`
  - `asset_id`: references a known synthetic asset
  - `title`: concise demo task title
  - `status`: `open | in_progress | resolved`
  - `priority`: `low | medium | high | critical`
  - `opened_at`: ISO timestamp
  - `resolved_at`: ISO timestamp or null
  - `linked_finding_ids`: list of deterministic finding IDs
  - `technician_action`: demo remediation action
  - `verification`: demo verification result

- Optional `Device` additions, only if needed:
  - `patch_deployed_at`: ISO timestamp or null
  - `maintenance_window`: short fake value such as `demo-weeknight`

Keep these in the committed synthetic fixture. Do not add generated or real-world IDs.

## Scoring model design

Preserve existing finding-based scoring, then add correlation outputs rather than a black-box score.

Recommended additions:

1. Vulnerability findings
   - Critical/high open vulnerability with patch available: high or critical finding.
   - Open vulnerability on privileged user's device: escalate severity or add correlated finding.
   - Remediated vulnerability: excluded from active findings but counted in risk-reduction demo.

2. Remediation queue
   - Open ticket age beyond a demo threshold: medium/high finding or queue priority boost.
   - Ticket linked to high/critical endpoint finding: high priority.
   - Resolved ticket contributes to before/after risk reduction.

3. Owner-centric risk
   - Device owned by privileged/tier0 user plus noncompliance, missing patch, or vulnerability: correlated high finding.
   - Disabled/stale user with assigned active device remains lifecycle risk.

4. Risk reduction summary
   - Before count/score: unresolved active findings plus open remediation.
   - After count/score: hypothetical or fixture-backed remediated state.
   - Output must be deterministic and explainable; avoid ML/LLM scoring.

Use transparent weights only if a numeric score is necessary. Prefer evidence lists and priorities because they are more explainable in interviews.

## Dashboard/demo workflows

The dashboard should support these reviewer workflows:

1. **Top risky endpoints**
   - Show endpoints ranked by active findings, highest severity, owner context, and patch/vulnerability state.

2. **Risk by identity owner**
   - Show user/owner, privilege level, assigned devices, endpoint compliance, MFA/disabled/stale context, and linked high-risk findings.

3. **Patch/vulnerability priority board**
   - Show open vulnerabilities or patch gaps sorted by severity, owner sensitivity, patch availability, and remediation status.

4. **Remediation queue**
   - Show ticket-style tasks with status, priority, linked assets/findings, action, and verification.

5. **Before/after risk reduction**
   - Show a simple scenario: privileged/sensitive user + noncompliant endpoint + missing critical patch/vulnerability → remediation ticket → improved risk state.

## Security and privacy notes

- All data must remain `synthetic-demo-data-only`.
- Use fake domains such as `example.test` or `example.com`; avoid production-like names.
- Do not include real employer names, real hostnames, real screenshots, tenant IDs, device IDs, personal emails, ticket IDs, secrets, or internal process details.
- Do not add real integrations in this lane.
- Do not publish, deploy, push, or alter external services without explicit approval.
- Dashboard JavaScript must continue escaping displayed values before inserting into HTML.
- Keep security claims honest: local demo, synthetic data, deterministic scoring, not production-grade EDR/IAM tooling.

## Acceptance criteria

- Existing tests pass from an installed external virtualenv.
- New behavior has meaningful tests written before implementation where practical.
- Synthetic data relationships validate and are obviously fake.
- Risk scoring is deterministic and tested.
- Static exporter includes dashboard-required data without real/private content.
- Browser dashboard visibly connects endpoint, identity owner, patch/vulnerability priority, remediation queue, and risk reduction.
- README/docs explain the demo in under 60 seconds.
- SECURITY/docs clarify local-only synthetic scope and non-goals.
- Final gate runs lint, strict source lint, format-check, typecheck, tests, and security scan where available.
- Findings are classified as fixed, accepted risk, false positive, environment/tooling-only, or deferred.
- No GitHub push, public deployment, repo creation, or external account change occurs without explicit approval.

## Validation plan

Set up environment outside the repo:

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

During implementation:

```bash
python -m pytest tests/test_demo_data.py -q
python -m pytest tests/test_risk.py -q
python -m pytest tests/test_static_demo.py -q
python scripts/export_static_demo.py
python -m json.tool site/demo-data.json >/dev/null
```

Before acceptance:

```bash
make lint
make lint-src-strict
make format-check
make typecheck
make test
make security
make all
```

Supplemental hygiene:

```bash
gitleaks detect --source . --no-git --redact
python -m bandit -q -r src
```

If any command fails, classify the finding rather than hiding it. Ahem.