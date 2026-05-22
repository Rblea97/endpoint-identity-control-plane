# Validation Log

**Date:** 2026-05-21
**Change/lane:** secure Python service template public-readiness hardening
**Classification:** ci-cd, security-control, public-release
**Branch/commit:** template directory, not a git repo

## Scope

- Objective: harden the reusable secure Python service template for repeatable Hermes/Codex SDLC work and eventual public GitHub readiness.
- In scope: template docs, Makefile gates, GitHub Actions workflow, CODEOWNERS, publication policy, validation templates, starter service quality fixes.
- Out of scope: cloud deployment, public publication, package publishing, container registry push, new MCP servers.
- Security-sensitive assumptions: template examples must remain fake/local; public release requires explicit Richie approval.

## Commands run

```text
actionlint /root/.hermes/project-templates/secure-python-service/.github/workflows/ci.yml
# result: PASS

python3 -m venv /tmp/secure-python-template-venv
. /tmp/secure-python-template-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
make all
actionlint .github/workflows/*.yml
# first result: FAIL, strict source lint found missing module/function docstrings

make all
actionlint .github/workflows/*.yml
# second result: FAIL, tests found missing httpx dev dependency for FastAPI/Starlette TestClient

make all
actionlint .github/workflows/*.yml
# third result: PASS

make public-release-check
# result: PASS
```

## Results

- Lint: PASS
- Strict source lint: PASS after adding starter app docstrings
- Format: PASS
- Typecheck: PASS
- Tests: PASS, `1 passed`
- Security/dependency scan: PASS; pip-audit reported no known vulnerabilities and skipped the local unpublished template package as expected
- Secret scan: PASS, gitleaks found no leaks
- Workflow lint: PASS

## Findings

- Finding: starter `src/endpoint_identity_control_plane/app.py` lacked public module/function docstrings.
  - Classification: fixed
  - Evidence: Ruff strict source lint failed with D100 and D103.
  - Decision: add useful starter docstrings instead of weakening strict public-quality gate.

- Finding: `httpx` missing from dev dependencies even though tests use FastAPI/Starlette `TestClient`.
  - Classification: fixed
  - Evidence: pytest failed with `RuntimeError: The starlette.testclient module requires the httpx package to be installed.`
  - Decision: add `httpx>=0.28,<1.0` to dev dependencies.

- Finding: prior security target treated gitleaks and pip-audit as non-blocking.
  - Classification: fixed
  - Evidence: Makefile used `|| true` for both.
  - Decision: split `security-advisory` from `security-blocking`; make `public-release-check` use blocking scans.

## Learning loop

- What worked: strict local gates immediately caught real starter-template issues before any public GitHub use.
- What failed or created noise: the template directory was not a git repo, so publication-gate validation needed a scaffold/private-repo rehearsal. The first scaffold run showed `hermes-publication-gate` was too strict because it blocked tracked `.env.example` placeholder files.
- What Codex did well: not applicable; Hermes implemented this lane directly because the changes were mostly templates/docs/gates.
- Where Codex drifted or guessed: not applicable in this lane.
- What Hermes caught: missing docstrings, missing `httpx`, advisory-vs-blocking scan ambiguity, the publication-gate `.env.example` false positive, missing `.gitignore` coverage for generated `*.egg-info/` plus `.hermes/reports/` artifacts, a GitHub-hosted runner PATH issue for `go install`ed `actionlint`, a GitHub Actions Node 20 deprecation warning for older action major versions, and ungrouped Dependabot PR noise in private scaffold rehearsals.
- What should be adapted: keep strict source lint in default template; keep out-of-repo venv validation; allow safe tracked placeholder env files in `hermes-publication-gate`; ignore generated package metadata and scan reports; call Go-installed tools by explicit path in GitHub Actions or add the Go bin path to `$GITHUB_PATH`; verify current GitHub Action major versions before publishing template workflows; group/limit Dependabot updates; use private scaffold repo to validate GitHub Actions and publication gates.

## Residual risk and rollback

- Residual risks: GitHub Actions workflow has local syntax validation but has not yet been executed on GitHub-hosted runners after these changes.
- Rollback path: revert template file changes from this lane or restore from the previous template snapshot if needed.
- Follow-up items: create a private GitHub rehearsal repo from the template and watch CI once local validation is clean.
