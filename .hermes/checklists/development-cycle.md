# Repeatable Development Cycle Checklist

Use this checklist for every meaningful AI-assisted development lane in this repo. It is intentionally more detailed than a normal TODO list because this project is a rehearsal for public GitHub and production-shaped work.

## 1. Intake and scope

- [ ] The lane has one clear objective.
- [ ] The expected user or reviewer value is stated.
- [ ] In-scope files/areas are identified.
- [ ] Out-of-scope files/areas are identified.
- [ ] Security-sensitive assumptions are listed.
- [ ] No real employer, customer, employee, incident, or personally sensitive data is needed.

## 2. Durable source of truth

- [ ] `AGENTS.md` has been read before implementation.
- [ ] The current design/spec/plan under `.hermes/plans/` has been read.
- [ ] The lane acceptance criteria are written in a repo file, not only in chat.
- [ ] A validation log will be added under `.hermes/plans/` if the lane changes code, docs, checks, or risk posture.

## 3. Codex lane preparation

Use `.hermes/templates/codex-lane-prompt.md` when Codex is asked to implement.

- [ ] Codex prompt has an exact goal.
- [ ] Codex prompt includes the exact known failing command/output or says there is no current failure.
- [ ] Codex prompt lists allowed files/areas.
- [ ] Codex prompt lists forbidden/out-of-scope changes.
- [ ] Codex prompt requires tests or explains why tests are not applicable.
- [ ] Codex prompt includes security constraints.
- [ ] Codex prompt requires exact validation commands and results.
- [ ] Codex prompt tells Codex which repo virtualenv/tool environment to activate, or explicitly says none is required.
- [ ] Codex prompt requires assumptions, risks, and files changed in the final summary.

## 4. Implementation discipline

- [ ] Changes are narrow and reviewable.
- [ ] No unrelated formatting churn.
- [ ] No unapproved new dependencies.
- [ ] Public behavior is unchanged unless explicitly required.
- [ ] Tests prove behavior, not just coverage.
- [ ] Cross-cutting controls/middleware are tested on non-happy paths, such as 404s, handled errors, unhandled 500s, blocked requests, and privacy-sensitive failures.
- [ ] Container/config tests parse or normalize semantics where practical instead of only checking raw strings; they should prove final runtime user, localhost-only exposure, no privileged/socket/host-networking config, and intended hardening controls.
- [ ] Fake/example data cannot be mistaken for real data.

## 5. Hermes review gate

Before accepting the lane:

- [ ] Diff reviewed for unrelated changes.
- [ ] Spec/plan alignment reviewed.
- [ ] Test quality reviewed.
- [ ] Security implications reviewed.
- [ ] README/docs/config drift reviewed.
- [ ] Findings are classified as fixed, accepted risk, false positive, tooling/environment issue, or deferred backlog.

## 6. Validation commands

Run the strongest practical gate for the lane.

For this repo, the default is:

```bash
make all
```

For docs-only lanes, still run `make all` unless there is a clearly documented reason not to.

Record results:

- [ ] Lint result recorded.
- [ ] Format-check result recorded.
- [ ] Type/static-analysis result recorded.
- [ ] Test result recorded.
- [ ] Security/dependency/secret scan result recorded.
- [ ] Any expected scanner note is classified.

## 7. Public GitHub readiness check

If the lane affects public-facing files:

- [ ] README still passes the 60-second skim test.
- [ ] Tone sounds like a real engineer, not generated portfolio filler.
- [ ] Architecture/security/ADR links still make sense.
- [ ] Limitations are honest and current.
- [ ] Docs distinguish implemented controls from future production controls.
- [ ] Public issues/docs do not ask people to disclose secrets or real sensitive data.

## 8. Commit and handoff

- [ ] Working tree reviewed with `git diff --stat` and focused diff inspection.
- [ ] Commit message is conventional and specific.
- [ ] Final summary includes what changed, validation, security findings, residual risks, and next lane.
- [ ] Any reusable workflow lesson is added to a skill, template, checklist, or repo rule.
