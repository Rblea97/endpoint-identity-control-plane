# Lane 7 Actionable IT Operations Demo Layer Implementation Plan

> **For Hermes:** Use TDD for CLI/demo behavior and keep the scope job-adjacent to entry-level IT, SCCM/MECM, Active Directory, imaging, endpoint support, and identity hygiene.

**Goal:** Turn the existing backend-focused project into a reviewer-friendly endpoint/identity operations lab with terminal demos, scenario runbooks, and a clear 5-minute demo path.

**Architecture:** Add a small pure-Python demo workflow module that maps deterministic findings to IT operations scenarios. Add a CLI entry point that prints technician-facing triage reports from synthetic data only. Add scenario markdown files that make the operational value visible without requiring real Microsoft systems.

**Tech Stack:** Python 3.11, existing Pydantic inventory/risk models, argparse/stdout CLI, pytest, Ruff, mypy.

---

## Scope

In scope:

1. `endpoint_identity_control_plane.operations_demo` module.
2. `endpoint-identity-demo` console script.
3. Scenario docs under `docs/demo-scenarios/`.
4. README update with a 5-minute actionable demo.
5. Tests for scenario listing, scenario reports, CLI output, and unknown scenario handling.

Out of scope:

1. Live Microsoft integrations.
2. Real AD/SCCM/Intune data.
3. Browser dashboard.
4. Database/authentication.
5. Public visibility change.

## Scenario set

Implement four scenarios:

1. `failed-imaging` — failed imaging / provisioning triage for `DEMO-LAPTOP-003`.
2. `disabled-user-device-assignment` — disabled user still assigned to device.
3. `privileged-user-missing-mfa` — privileged account without MFA.
4. `endpoint-compliance-queue` — prioritized endpoint remediation queue.

## Tasks

### Task 1: Add failing tests for operations demo API

**Files:**
- Create: `tests/test_operations_demo.py`

**Steps:**
1. Import wished-for functions from `endpoint_identity_control_plane.operations_demo`.
2. Assert listed scenarios include the four scenario IDs.
3. Assert `build_scenario_report("failed-imaging")` includes a ticket summary, affected device hostname, findings, and technician actions.
4. Assert unknown scenario IDs raise `ValueError`.
5. Run `python -m pytest tests/test_operations_demo.py -q` and verify RED failure because module does not exist.

### Task 2: Implement operations demo module

**Files:**
- Create: `src/endpoint_identity_control_plane/operations_demo.py`

**Steps:**
1. Define frozen dataclasses for scenario metadata and generated reports.
2. Load committed synthetic inventory through `load_demo_inventory()`.
3. Build risk findings with existing deterministic `evaluate_inventory()` and fixed demo timestamp.
4. Implement scenario report builders that return technician-facing text sections.
5. Keep all data synthetic and sourced from existing fixture/models.
6. Run targeted tests and full tests.

### Task 3: Add failing CLI tests

**Files:**
- Modify: `tests/test_operations_demo.py`
- Modify: `pyproject.toml`

**Steps:**
1. Add tests for `main(["--list"])` and `main(["--scenario", "failed-imaging"])`.
2. Add expectation that output contains the scenario ID, ticket, affected asset, findings, and technician actions.
3. Run targeted tests and verify failure because CLI main/entrypoint does not exist yet.

### Task 4: Implement CLI entry point

**Files:**
- Modify: `src/endpoint_identity_control_plane/operations_demo.py`
- Modify: `pyproject.toml`

**Steps:**
1. Add `main(argv: list[str] | None = None) -> int` with argparse.
2. Support `--list` and `--scenario <id>`.
3. Add project script `endpoint-identity-demo = "endpoint_identity_control_plane.operations_demo:main"`.
4. Ensure CLI returns nonzero on unknown scenario and prints a helpful error.
5. Run targeted CLI tests.

### Task 5: Add scenario docs

**Files:**
- Create: `docs/demo-scenarios/README.md`
- Create: `docs/demo-scenarios/01-failed-imaging-triage.md`
- Create: `docs/demo-scenarios/02-disabled-user-device-assignment.md`
- Create: `docs/demo-scenarios/03-privileged-user-missing-mfa.md`
- Create: `docs/demo-scenarios/04-endpoint-compliance-queue.md`

**Steps:**
1. Explain the fake ticket, what the demo checks, expected evidence, technician actions, verification, and resume/interview talking point for each scenario.
2. Keep language public-safe and explicit that this simulates workflow thinking, not live tenant administration.

### Task 6: Update README for practical value

**Files:**
- Modify: `README.md`

**Steps:**
1. Add “5-minute actionable IT demo” section near quick start.
2. Add exact commands:
   - `endpoint-identity-demo --list`
   - `endpoint-identity-demo --scenario failed-imaging`
   - `endpoint-identity-demo --scenario endpoint-compliance-queue`
3. Reframe value as an endpoint operations lab, not just an API repo.
4. Update roadmap to mark Lane 7 completed.

### Task 7: Validate, commit, push, PR

**Commands:**

```bash
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -e '.[dev]'
make all
git diff --check
git status --short
git add .
git commit -m "feat: add actionable IT operations demos"
git push -u origin feat/actionable-it-demo-layer
gh pr create --title "feat: add actionable IT operations demos" --body "..."
```

**Verification:**
- Targeted tests pass.
- Full local validation passes.
- CI passes on PR.
- Repo remains private unless Richie explicitly approves public visibility.
