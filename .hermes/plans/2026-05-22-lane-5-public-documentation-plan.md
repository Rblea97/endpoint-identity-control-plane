# Lane 5 Public Documentation Foundation Plan

> **For Hermes:** Keep this lane documentation-only unless a validation command exposes stale behavior claims that require a small corrective patch.

**Goal:** Turn the working backend MVP into a reviewer-friendly portfolio artifact with accurate public documentation, architecture context, API examples, security posture, threat model, ADRs, and interview narrative.

**Architecture:** The service remains a local FastAPI API backed by committed synthetic JSON inventory and a deterministic in-process risk engine. This lane documents the implemented service boundary and explicitly defers live demo, authentication, persistence, and real Microsoft integrations.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, pytest, Ruff, mypy, Bandit, Gitleaks, pip-audit.

---

## Scope

### In scope

- Update `README.md` so a hiring manager can understand the project quickly.
- Replace placeholder architecture/API/security/threat-model docs with project-specific docs.
- Add ADR index and project-specific ADRs for key decisions.
- Add a portfolio/interview narrative that is honest and job-adjacent.
- Record validation evidence after docs are updated.

### Out of scope

- Dashboard/UI implementation.
- Live deployment.
- Authentication/authorization.
- Persistence/database work.
- Real Active Directory, SCCM/MECM, Intune, Entra ID, Defender, Microsoft Graph, or employer data integrations.
- VM lab setup.

## Tasks

### Task 1: README refresh

**Objective:** Update the README to match implemented API behavior after Lane 4.

**Files:**

- Modify: `README.md`

**Verification:**

- README first screen explains the project, fake-data status, skills demonstrated, quick start, and example output.
- No claims of production readiness or real Microsoft integration.

### Task 2: Deep docs refresh

**Objective:** Replace placeholder docs with accurate project documentation.

**Files:**

- Modify: `docs/architecture.md`
- Modify: `docs/api.md`
- Modify: `docs/security-posture.md`
- Modify: `docs/threat-model.md`
- Modify: `docs/portfolio-narrative.md`

**Verification:**

- Docs describe actual endpoints, request flow, trust boundaries, controls, limitations, and portfolio narrative.
- Docs state `synthetic-demo-data-only` where data-handling matters.

### Task 3: ADR pass

**Objective:** Add decision records for the key public-facing architecture choices.

**Files:**

- Create: `docs/adr/README.md`
- Modify: `docs/adr/0001-use-fastapi.md`
- Create: `docs/adr/0002-use-synthetic-demo-data.md`
- Create: `docs/adr/0003-use-deterministic-risk-rules.md`
- Create: `docs/adr/0004-defer-vm-lab-and-real-integrations.md`

**Verification:**

- ADRs include status, context, decision, considered options, rationale, consequences, and revisit criteria.
- ADRs distinguish local/demo controls from deferred production controls.

### Task 4: Validate docs lane

**Objective:** Confirm docs did not drift from behavior and record results.

**Commands:**

```bash
git diff --check
. /tmp/endpoint-identity-control-plane-venv/bin/activate
make all
```

**Files:**

- Create: `.hermes/checklists/2026-05-22-lane-5-validation.md`

**Expected result:**

- Whitespace check passes.
- Full local gate passes.
- Any known advisory scan note is classified.
