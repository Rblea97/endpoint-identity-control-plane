# Public Release Readiness Checklist

Use this before making a repo public, portfolio-facing, or production-shaped beyond a private sandbox.

## Code style and typing

- [ ] Ruff baseline is documented and appropriate for public-facing Python.
- [ ] Ruff pydocstyle uses Google convention for production code.
- [ ] Public modules/classes/functions in `src/` have useful docstrings.
- [ ] Route handlers and security-sensitive helpers document behavior and assumptions.
- [ ] PEP 484 type coverage is meaningful; tests are typechecked or exclusion is justified.
- [ ] Any `Any`, `type: ignore`, or `noqa` usage is local and justified.
- [ ] Line length policy is documented and consistently enforced.

## Public documentation

- [ ] README includes a concrete one-line description, status/scope line, useful badges, quick start, example output, architecture overview, and links to detailed docs.
- [ ] README or docs include Mermaid system/request-flow diagrams.
- [ ] README links to `/docs`, `/redoc`, and `/openapi.json` when FastAPI is used.
- [ ] API docs include success and error examples.
- [ ] Configuration reference lists all supported env vars and defaults.
- [ ] `.env.example` matches supported settings and contains placeholders only.
- [ ] `docs/public-repo-file-policy.md` has been applied to `AGENTS.md`, `.hermes/`, generated artifacts, and local reports.
- [ ] Docs distinguish implemented controls from future production controls.
- [ ] Known limitations and production-readiness roadmap are honest and current.

## Architecture and decisions

- [ ] `docs/architecture.md` exists.
- [ ] `docs/diagrams/` contains Mermaid source diagrams or non-use is justified.
- [ ] `docs/adr/0000-template.md` exists.
- [ ] ADRs exist for major technology/security decisions.
- [ ] Technology-choice rationale is explicit and interview-useful.

## Security and public posture

- [ ] `docs/security-posture.md` exists.
- [ ] `docs/threat-model.md` exists.
- [ ] SECURITY.md defines reporting expectations or clearly states private handling.
- [ ] SECURITY.md tells reporters not to include sensitive data in public issues.
- [ ] Security/dependency/container scan status is current before release.

## Portfolio/interview readiness

- [ ] `docs/portfolio-narrative.md` exists when this is a portfolio project.
- [ ] Docs explain why this is more than CRUD.
- [ ] Docs explain major tradeoffs and what would change for production.
