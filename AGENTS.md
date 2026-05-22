# AGENTS.md

## Project purpose

[Replace this with 3-5 sentences describing the project, its users, and what it must not do.]

## Tech stack

- Language: Python 3.11+
- Framework: FastAPI or service/CLI modules as needed
- Package manager: pip + pyproject.toml
- Runtime: local Python; container optional
- Deployment target: local/private sandbox unless explicitly changed
- Infrastructure tools: GitHub Actions; Docker optional

## Important directories

- `src/`: Application source code.
- `tests/`: Unit and integration tests.
- `docs/`: User/developer docs and decision records.
- `.hermes/plans/`: Durable specs and implementation plans. Use this to survive chat compaction.
- `.hermes/checklists/`: Acceptance, readiness, development-cycle, and public GitHub review checklists.
- `.hermes/templates/`: Reusable agent/Codex prompt templates for repeatable development lanes.
- `.github/workflows/`: CI workflows. Keep permissions least-privilege.

## Build, test, lint, and scan commands

Run these before claiming completion:

```bash
make test
make lint
make typecheck
make security
make all
```

If a command fails because project dependencies are not installed, report that explicitly and include the install command used.

## Coding conventions

- AI-generated code is untrusted until independently reviewed and verified.
- Keep changes small and reviewable.
- Prefer clear, boring code over clever code.
- Preserve public interfaces unless the task explicitly requires a change.
- Add or update meaningful tests for behavior changes.
- Do not change unrelated files.
- Do not introduce new dependencies without explaining why.
- Keep functions focused; avoid god functions and premature abstractions.
- For public-facing or portfolio-grade Python code, phase in PEP 8, PEP 257, PEP 484, and Google-style docstring expectations using Ruff and mypy.
- Do not claim public readiness just because the private/sandbox gate passes; check the public-readiness checklist first.

## Security rules

- Do not hardcode secrets, tokens, passwords, private keys, or real personal data.
- Do not log secrets or sensitive request bodies.
- Validate external input at boundaries.
- Use least privilege for files, CI permissions, credentials, and services.
- Avoid unsafe shell execution. If shell execution is required, document why and validate inputs.
- Prefer secure defaults and explicit configuration.
- Document security-sensitive assumptions and residual risk.

## DevSecOps rules

For CI/CD, container, infrastructure, or deployment changes:

- Explain deployment impact.
- Identify required secrets/permissions by name only, never by value.
- Include rollback guidance.
- Include verification steps.
- Keep GitHub Actions permissions minimal.
- Re-run dependency/security scans after workflow or dependency changes.

## Codex lane policy

When Codex is used:

- Hermes writes or references the task spec first.
- Codex receives a narrow implementation lane, not the entire project mission.
- Codex must run the listed verification commands or clearly state why it could not.
- Codex returns: files changed, tests run, results, assumptions, and risks.
- Codex must not claim success unless verification was actually performed.

## Context and compaction policy

- Do not rely on chat context for project state.
- Save approved specs to `.hermes/plans/`.
- Save decisions to `docs/adr/` or `.hermes/plans/`.
- Save final validation results to `.hermes/checklists/` or `docs/`.
- For public-facing projects, create architecture docs, Mermaid diagrams, ADRs, security posture, threat model, and portfolio/interview narrative before claiming release readiness.
- Before implementation after a long chat, read the current plan files rather than trusting memory.

## Done when

Work is complete only when:

- The requested change is implemented.
- Required tests/verification pass, or failures are clearly explained.
- Security implications and residual risks are reviewed.
- Docs/checklists are updated if behavior, setup, or risk changed.
- The diff is summarized.
- No secrets or sensitive data are introduced.
