# Public Repository File Policy

Use this policy before making a repository public or using it as portfolio evidence. The goal is to keep public repositories useful to humans while avoiding accidental publication of secrets, private planning, or noisy generated artifacts.

## Ground rules

- Public repos should read like intentional software projects, not raw AI workspaces.
- Human-facing docs belong in `README.md`, `SECURITY.md`, and `docs/`.
- Agent-facing instructions can be public when sanitized and useful, especially `AGENTS.md`.
- Generated files, local reports, raw prompts, transcripts, and private retrospectives should stay out of public repos unless deliberately rewritten for public learning value.
- If a file would embarrass, confuse, or expose private process details to a recruiter, hiring manager, senior engineer, or security reviewer, rewrite it or keep it private.

## File-by-file guidance

### Usually public

- `README.md`: human overview, quick start, examples, architecture links, limitations.
- `LICENSE` / `LICENSE.md`: required if the repo is meant to be reusable as open source.
- `SECURITY.md`: reporting expectations and safe disclosure guidance.
- `.gitignore`: shared ignore rules for the project.
- `.github/workflows/`: CI/CD definitions, reviewed for least privilege.
- `.github/dependabot.yml`: dependency update strategy.
- `.github/PULL_REQUEST_TEMPLATE.md` and issue templates: useful for public collaboration.
- `.github/CODEOWNERS`: useful when it documents ownership for sensitive paths.
- `docs/architecture.md`, `docs/api.md`, `docs/testing.md`, `docs/security-posture.md`, `docs/threat-model.md`: public engineering evidence when accurate and sanitized.
- `docs/adr/`: public when decisions are written professionally and do not expose private/employer/customer details.
- `.env.example`, `.env.sample`, `.env.template`: public only when every value is fake or clearly a placeholder.
- `AGENTS.md`: public when it contains build/test/style/security instructions and no secrets, private strategy, or raw prompt content.

### Sometimes public after review

- `.hermes/checklists/`: public if the checklist helps reviewers understand quality gates and contains no private operational details.
- `.hermes/templates/`: public if the prompt templates are generic, sanitized, and useful for repeatable development.
- `.hermes/plans/`: public only for polished design specs or implementation plans that help explain the project. Keep raw scratch plans private.
- `docs/portfolio-narrative.md`: public if it reads like an interview prep note or project rationale, not inflated marketing copy.
- Mermaid diagrams or screenshots: public only if they use fake data and do not reveal account IDs, private hosts, tokens, usernames, ticket data, or employer/customer details.

### Usually private or ignored

- `.env` and any config file with real values.
- Credentials, tokens, cookies, session files, private keys, cloud credentials, kubeconfigs, or SSH material.
- Raw AI chat transcripts, scratch prompts, failed prompt attempts, and private retrospectives.
- `.hermes/reports/`, scanner outputs, SARIF files, SBOMs, coverage HTML, and local validation logs unless intentionally published after review.
- Virtualenvs, caches, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `*.egg-info/`, build artifacts, local databases, and logs.
- Real tickets, incident data, employer/customer details, internal hostnames, private IPs, emails, cloud account IDs, ARNs, tenant IDs, subscription IDs, or billing data.

## AGENTS.md public guidance

`AGENTS.md` is acceptable in public repositories when it acts as a README for coding agents:

- setup commands;
- test/lint/security commands;
- project conventions;
- safe coding rules;
- done criteria;
- boundaries for agent changes.

Keep it public-safe:

- do not include private credentials, names of private systems, or internal escalation paths;
- do not include raw chat history or prompt experiments;
- do not include instructions that would let an agent bypass review, CI, secret scanning, or human approval;
- keep human project value in `README.md` so agent instructions do not clutter the public overview.

## `.hermes/` public guidance

A `.hermes/` directory can be useful public evidence when it shows disciplined engineering workflow, but it should be curated.

Recommended public subset:

```text
.hermes/
  checklists/
    public-github-review.md
    public-release-readiness.md
    validation-log-template.md
  templates/
    codex-lane-prompt.md
  publication-policy.yml
```

Review carefully before publishing:

```text
.hermes/plans/
```

Usually ignore or keep private:

```text
.hermes/reports/
.hermes/tmp/
.hermes/cache/
raw transcripts
scratch prompts
private retrospectives
```

## Pre-publication review questions

Before publishing, ask:

1. Does this file help a human understand, run, review, or trust the project?
2. Does this file help future agents work safely without cluttering the README?
3. Could this file reveal private process, credentials, customer/employer data, infrastructure identifiers, or personal data?
4. Would this look intentional to a recruiter or senior engineer in a 60-second skim?
5. If the repo were forked today, would this file still be safe and useful?

If the answer is uncertain, keep the file private until it is rewritten or sanitized.
