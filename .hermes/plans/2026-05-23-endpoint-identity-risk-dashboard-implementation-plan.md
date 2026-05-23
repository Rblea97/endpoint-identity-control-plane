# Endpoint + Identity Risk Dashboard Implementation Plan

> **For Hermes:** Use this plan task-by-task. Use TDD for behavior changes. Do not commit, push, deploy, create a repo, or trigger GitHub Pages without Richie's explicit approval.

**Goal:** Implement the next portfolio-grade lane for Endpoint Identity Control Plane: a synthetic Endpoint + Identity Risk Dashboard with patch/vulnerability priority, remediation queue, and before/after risk reduction.

**Architecture:** Extend the current strict Pydantic inventory models, committed synthetic fixture, deterministic risk engine, static exporter, vanilla browser dashboard, and docs. Avoid new dependencies and preserve existing FastAPI/CLI behavior.

**Tech Stack:** Python 3.11, Pydantic v2, FastAPI, pytest, Ruff, mypy, Bandit, pip-audit, vanilla HTML/CSS/JavaScript.

---

## Pre-flight

Workdir:

```bash
cd /root/workspace/endpoint-identity-control-plane
```

Use an external virtualenv so scans do not audit in-repo tooling artifacts:

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

Baseline checks after install:

```bash
make test
make lint
make typecheck
```

Expected current-state note from inspection:

- `PYTHONPATH=src python3 -m pytest tests -q` passed with `34 passed` before this plan.
- Raw `make test` failed only because the shell environment had not installed the package.

## Files likely to change

Modify:

- `src/endpoint_identity_control_plane/models.py`
- `src/endpoint_identity_control_plane/data/demo/inventory.json`
- `src/endpoint_identity_control_plane/risk.py`
- `scripts/export_static_demo.py`
- `site/index.html`
- `site/styles.css`
- `site/app.js`
- `site/demo-data.json`
- `tests/test_demo_data.py`
- `tests/test_risk.py`
- `tests/test_static_demo.py`
- `README.md`
- `docs/architecture.md`
- `docs/security-posture.md` or `SECURITY.md` if security/non-goal wording changes

Possibly modify:

- `src/endpoint_identity_control_plane/app.py` if `/risk-report` needs to expose new summary fields through the existing model.
- `docs/demo-scenarios/README.md` if adding a new scenario walkthrough.
- `docs/api.md` if API response examples change.

Do not modify without explicit approval:

- `.github/workflows/pages.yml` deployment behavior.
- Remote configuration, repo visibility, or branch protection.
- Any real integration secrets or external service configuration.

## Implementation lanes

### Lane 1: Environment baseline and source-of-truth check

**Objective:** Establish a clean installed baseline before changing behavior.

**Steps:**

1. Activate/install external venv using pre-flight commands.
2. Run `git status --short --branch`.
3. Run `make test`, `make lint`, and `make typecheck`.
4. Record any baseline failures in the final response or a validation log.

**Verification:**

```bash
git status --short --branch
make test
make lint
make typecheck
```

### Lane 2: Add strict synthetic vulnerability and remediation models with tests

**Objective:** Extend `Inventory` to validate vulnerability and remediation records.

**Files:**

- Modify: `src/endpoint_identity_control_plane/models.py`
- Modify: `tests/test_demo_data.py`

**TDD steps:**

1. Add failing tests that expect loaded demo inventory to expose `vulnerability_records` and `remediation_tickets`.
2. Add tests that invalid `device_id`, `asset_id`, and `linked_finding_ids` relationships are rejected where practical.
3. Run targeted tests and confirm failure.
4. Add minimal Pydantic models and `Inventory` fields.
5. Add relationship validation for vulnerability device IDs and remediation asset references.
6. Run targeted tests and then full tests.

**Commands:**

```bash
python -m pytest tests/test_demo_data.py -q
python -m pytest tests -q
```

### Lane 3: Expand committed synthetic fixture

**Objective:** Add obviously fake vulnerability and remediation examples that tell the demo story.

**Files:**

- Modify: `src/endpoint_identity_control_plane/data/demo/inventory.json`
- Modify: `tests/test_demo_data.py`

**Data guidance:**

- Use IDs like `vuln-001`, `vuln-002`, `ticket-001`.
- Use fake domains only; current data uses `example.example`, which is synthetic but awkward. Prefer new values as `example.test` or `example.com` if touching usernames.
- Keep hostnames like `DEMO-WIN11-002`, not real hostnames.
- Include at least:
  - open critical/high vulnerability on `device-002` owned by privileged `user-002`;
  - open high/critical patch/vulnerability issue on `device-003` to preserve top risky endpoint story;
  - remediated ticket that demonstrates before/after risk reduction;
  - open remediation queue item linked to high-risk finding(s).

**Verification:**

```bash
python -m pytest tests/test_demo_data.py -q
```

### Lane 4: Add deterministic correlation and risk-reduction outputs

**Objective:** Make endpoint + identity correlation explicit in the risk engine.

**Files:**

- Modify: `src/endpoint_identity_control_plane/risk.py`
- Modify: `tests/test_risk.py`

**TDD tests to add first:**

- Open critical/high vulnerability produces deterministic finding.
- Vulnerability on privileged user's device produces owner-context correlation finding or elevated severity.
- Open remediation ticket appears in a remediation queue summary.
- Resolved/remediated item reduces active risk in a deterministic risk-reduction summary.
- Existing deterministic behavior remains stable for same `as_of`.

**Implementation guidance:**

- Prefer explicit models such as `RemediationQueueItem` and `RiskReductionSummary` if they improve API/export clarity.
- Keep finding IDs stable and readable.
- Do not introduce ML-like or opaque scores.
- If adding numeric scoring, keep weights small and documented in code/tests.

**Verification:**

```bash
python -m pytest tests/test_risk.py -q
python -m pytest tests/test_api_endpoints.py -q
python -m pytest tests -q
```

### Lane 5: Extend static exporter payload

**Objective:** Feed the dashboard the owner risk, patch/vulnerability board, remediation queue, and risk-reduction data.

**Files:**

- Modify: `scripts/export_static_demo.py`
- Modify: `tests/test_static_demo.py`
- Regenerate: `site/demo-data.json`

**TDD tests to add first:**

- Payload includes `vulnerability_records` or `patch_vulnerability_board`.
- Payload includes `remediation_queue`.
- Payload includes `risk_reduction_summary`.
- Payload preserves `data_classification == synthetic-demo-data-only`.
- Payload contains no obvious private/employer strings.

**Verification:**

```bash
python -m pytest tests/test_static_demo.py -q
python scripts/export_static_demo.py
python -m json.tool site/demo-data.json >/dev/null
```

### Lane 6: Upgrade dashboard UI without adding dependencies

**Objective:** Make the static dashboard communicate the full portfolio story quickly.

**Files:**

- Modify: `site/index.html`
- Modify: `site/styles.css`
- Modify: `site/app.js`
- Modify: `tests/test_static_demo.py` if static asset requirements change

**UI sections to add or improve:**

1. Risk by identity owner.
2. Patch/vulnerability priority board.
3. Remediation queue.
4. Before/after risk reduction summary.
5. Short hero copy explaining synthetic/local Microsoft-style endpoint + identity workflow.

**Security requirement:**

- Continue escaping values before injecting dynamic content into the DOM.
- Do not use `innerHTML` with unescaped data. Current helper `escapeHtml` must remain in use for all dynamic values.

**Verification:**

```bash
python -m pytest tests/test_static_demo.py -q
python scripts/export_static_demo.py
python -m http.server 4173 --directory site
```

Then visually inspect `http://127.0.0.1:4173/` if browser access is available.

### Lane 7: Docs and portfolio proof

**Objective:** Ensure a recruiter/hiring manager can understand the artifact fast.

**Files:**

- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/api.md` if `/risk-report` shape changed
- Modify: `docs/security-posture.md` or `SECURITY.md` if scope/non-goals changed
- Possibly modify: `docs/portfolio-narrative.md`

**Docs must explain:**

- What the dashboard demonstrates.
- Why the data is synthetic and public-safe.
- How endpoint state, identity owner context, patch/vulnerability priority, and remediation connect.
- How to run the local demo.
- What is intentionally not production-grade.

**Verification:**

```bash
python -m pytest tests -q
```

Manual docs check:

- README explains the demo in under 60 seconds.
- No real employer, tenant, hostname, username, screenshot, ticket, or credential appears.

### Lane 8: Quality gate and public-readiness classification

**Objective:** Verify the lane before claiming completion.

**Commands:**

```bash
make lint
make lint-src-strict
make format-check
make typecheck
make test
make security
make all
gitleaks detect --source . --no-git --redact
```

Classify every finding as one of:

- fixed
- real project risk accepted with justification
- false positive with justification
- environment/tooling-only issue
- deferred with follow-up task

**Final response must include:**

- What changed.
- Files touched.
- Validation commands run.
- Results.
- Security findings/classifications.
- Residual risks.
- Next recommended step.

## Suggested Codex lane prompt template

Use Codex only after the spec and this implementation plan are committed or at least saved. Keep each task narrow.

```text
You are implementing one narrow lane in /root/workspace/endpoint-identity-control-plane.

Goal:
[one lane only]

In scope:
[exact files]

Out of scope:
- new repo
- real integrations
- deployment/publication
- broad refactor
- unrelated docs or workflow changes

Requirements:
[quote the relevant design/spec excerpt]

Testing:
- Write/update meaningful tests first where practical.
- Run the targeted commands below.

Commands:
[exact commands]

Return:
- files changed
- tests/checks run
- results
- assumptions
- risks
```

## Approval checkpoint

This plan extends models, fixture data, risk scoring, exporter payload, dashboard UI, and docs. That is within the requested lane, but it is still a meaningful multi-file implementation. Ask Richie before starting major implementation if he wants Hermes to execute directly or delegate narrow lanes to Codex.
