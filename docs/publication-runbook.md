# Publication Runbook

Use this before making the repository public, sharing it as portfolio evidence, publishing a package, pushing a container image, creating a release, or deploying beyond a private sandbox.

## Publication rule

No public push, public repo visibility change, package publish, container registry push, release, or deployment occurs without explicit Richie approval.

## 1. Confirm intent

- [ ] Repo is intended to be `private-lab`, `public-portfolio`, or `private-work`.
- [ ] `.hermes/publication-policy.yml` matches the intended visibility.
- [ ] This repo contains no employer, customer, internal system, real incident, or personal sensitive data.

## 2. Public safety review

Check for and remove or sanitize:

- `.env` files or real config values
- tokens, passwords, private keys, cookies, auth files, or session files
- real cloud account IDs, ARNs, tenant IDs, subscription IDs, billing data, private IPs, hostnames, or emails
- raw AI transcripts, scratch prompts, failed prompt attempts, private TODOs, or local notes
- unsanitized logs, screenshots, tickets, reports, SBOMs, SARIF files, or scanner output
- generated caches, virtualenvs, egg-info, coverage output, local databases, and build artifacts

Review these files intentionally rather than blindly including or excluding them:

- `AGENTS.md` is acceptable publicly when it contains sanitized setup/test/style/security instructions for coding agents.
- `.hermes/checklists/`, `.hermes/templates/`, and `.hermes/publication-policy.yml` are acceptable when generic, sanitized, and useful to reviewers.
- `.hermes/plans/` should be public only when plans are polished design artifacts. Raw scratch plans and retrospectives stay private.
- See `docs/public-repo-file-policy.md` for the file-by-file policy.

## 3. Documentation review

A reviewer should understand within 30-60 seconds:

- what the project is
- why it exists
- what skills it demonstrates
- how to run it locally
- what evidence proves it works
- what is intentionally lab-only or simulated

Required docs for public portfolio state:

- `README.md`
- `SECURITY.md`
- `docs/architecture.md`
- `docs/security-posture.md`
- `docs/threat-model.md`
- `docs/testing.md`
- `docs/development.md`
- `docs/change-management.md`
- `docs/portfolio-narrative.md` when used for portfolio/interview material

## 4. Technical release gate

Run:

```bash
make public-release-check
hermes-publication-gate --repo .
hermes-sec-scan --repo .
```

If containers exist, also run:

```bash
hadolint Dockerfile
trivy fs .
syft .
grype dir:.
```

## 5. GitHub controls

Before public publication:

- [ ] Branch protection is configured for `main`.
- [ ] Required status checks are enabled.
- [ ] PR review is required for public-facing changes.
- [ ] Force pushes and branch deletion are protected.
- [ ] Workflow/security/dependency files are covered by CODEOWNERS where appropriate.

## 6. Final approval

Record:

- [ ] final commit SHA
- [ ] validation commands and results
- [ ] unresolved findings or accepted risks
- [ ] rollback or unpublish path
- [ ] Richie approval

Do not proceed if approval is missing.
