# Public GitHub Review Checklist

Use this before publishing the repo, sharing it with a recruiter/hiring manager, or treating a milestone as portfolio-presentable.

## 60-second skim

A reviewer should be able to answer these within about one minute:

- [ ] What is this project?
- [ ] Why does it exist?
- [ ] What does it demonstrate technically?
- [ ] How do I run it locally?
- [ ] What does a successful request/response look like?
- [ ] Where are the architecture, API, security, and decision docs?
- [ ] What are the honest limitations?

## README quality

- [ ] The first screen has a plain project description and status/scope line.
- [ ] Value appears before deep caveats.
- [ ] The README includes 2-5 useful badges or no badges; it does not use a noisy badge wall.
- [ ] Badges reflect real checks, supported versions, or security posture after the repo exists.
- [ ] Quick start is short and accurate.
- [ ] Example request/response uses fake data only.
- [ ] If there is no live demo, the README uses an honest substitute: local URL, API example, screenshot, architecture diagram, or sample output.
- [ ] Headings are natural; no awkward meta-headings such as "Public-facing documentation".
- [ ] Wording does not sound like inflated AI marketing copy.

## Documentation structure

- [ ] `docs/architecture.md` explains the system shape and boundaries.
- [ ] `docs/api.md` explains endpoints and examples.
- [ ] `docs/security-posture.md` explains implemented controls and non-goals.
- [ ] `docs/threat-model.md` identifies assets, trust boundaries, threats, and mitigations.
- [ ] `docs/development.md` explains local setup and workflow.
- [ ] `docs/testing.md` explains the quality/security gates.
- [ ] `docs/portfolio-narrative.md` explains what the project demonstrates without overselling it.
- [ ] `docs/adr/` records meaningful decisions and tradeoffs.

## Security and data handling

- [ ] No secrets, tokens, private keys, internal hostnames, or real sensitive data are committed.
- [ ] `.env.example` uses safe placeholder values only.
- [ ] SECURITY guidance tells reporters not to include secrets or sensitive data in public issues.
- [ ] Logs and examples do not expose ticket bodies, auth headers, cookies, or arbitrary headers.
- [ ] Known limitations are explicit and current.

## Repository hygiene

- [ ] `.gitignore` excludes caches, virtualenvs, local reports, and secret-bearing env files.
- [ ] Generated artifacts are not present in the template or repo checkout before publication (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `*.egg-info/`, coverage output, local DBs, logs).
- [ ] `AGENTS.md` is sanitized and useful if public; otherwise it is excluded intentionally.
- [ ] `.hermes/` content is curated: generic checklists/templates/policies may be public, raw plans/prompts/reports stay private.
- [ ] `docs/public-repo-file-policy.md` has been reviewed for this repo.
- [ ] CI exists and uses least-privilege permissions.
- [ ] Dependabot or dependency update strategy exists.
- [ ] PR/issue templates exist if the repo is public or portfolio-facing.
- [ ] Commit history is understandable enough for review, or a release note summarizes the milestone.

## Final publication gate

- [ ] `make all` passes on a clean checkout or any failure is classified.
- [ ] Secret scan is clean.
- [ ] Dependency scan has no unclassified project vulnerabilities.
- [ ] Public README/docs were reviewed after the final diff.
- [ ] Residual risks are documented before publishing.
