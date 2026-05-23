# Change Management Guide

Use this guide for every meaningful change in this repository. The goal is not bureaucracy; the goal is a repeatable learning loop where Hermes and Codex discover what works, catch what fails, and improve the reusable development system.

## Change classifications

Classify each lane before implementation:

- `docs-only`
- `test-only`
- `code-behavior`
- `dependency`
- `ci-cd`
- `security-control`
- `container`
- `database/migration`
- `cloud/deployment`
- `public-release`

Higher-risk classifications require stronger review, validation, and rollback evidence.

## Required lifecycle

### 1. Intake and scope

Record:

- one clear objective
- expected user or reviewer value
- in-scope files and behavior
- out-of-scope files and behavior
- security-sensitive assumptions
- required validation commands
- rollback path for dependencies, CI/CD, persistence, containers, cloud, or deployment changes

### 2. Design checkpoint

Required for non-trivial code, CI/CD, security, persistence, container, cloud, or public-release changes. Save the design under `.hermes/plans/`, `docs/`, or `docs/adr/`.

Cover:

- assets
- trust boundaries
- inputs and outputs
- identities and permissions
- secrets and sensitive data
- external dependencies
- failure modes
- explicit non-goals

### 3. Implementation lane

When Codex is used, use `.hermes/templates/codex-lane-prompt.md`. Codex should receive one narrow lane, not the full project mission.

Rules:

- Keep the diff small and reviewable.
- Do not change unrelated files.
- Do not add dependencies without approval.
- Do not use real personal, employer, customer, incident, or secret data.
- Do not push, publish, release, deploy, or alter cloud resources unless Richie explicitly approves.
- For webhook/Kanban rehearsals, use docs-only draft PRs and verify capture-only behavior before any automation tier is promoted.

### 4. Hermes review gate

Before accepting a lane, review:

- diff focus
- spec compliance
- test quality and edge cases
- code maintainability
- security implications
- docs/config drift
- validation evidence
- scanner findings classification

Classify findings as one of:

- fixed
- accepted risk
- false positive
- environment/tooling issue
- deferred backlog

### 5. Validation

Default local gate:

```bash
make all
```

Before public release or publication:

```bash
make public-release-check
hermes-publication-gate --repo .
hermes-sec-scan --repo .
```

### 6. PR and release

Use branch + PR for public-facing work. Do not merge or publish until required checks pass and residual risks are documented. Public publication requires Richie's explicit approval.

## Learning loop

After each non-trivial lane, capture:

- what Codex did well
- where Codex drifted or guessed
- what Hermes caught
- which checks produced useful signal
- which checks created false-positive noise
- which template, skill, checklist, hook, or runbook should be improved

Use `.hermes/checklists/validation-log-template.md` for repeatable evidence capture.
