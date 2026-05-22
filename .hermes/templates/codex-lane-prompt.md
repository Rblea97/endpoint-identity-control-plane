# Codex Lane Prompt Template

Use this template when Hermes delegates a narrow implementation lane to Codex.

```text
You are Codex working in the repository at: [ABSOLUTE_REPO_PATH]

Goal:
[One sentence: what to implement or update.]

Why this matters:
[One or two sentences explaining user/project value.]

Read first:
- AGENTS.md
- [specific plan/spec/checklist files]
- [specific source/test/docs files relevant to the lane]

Known failing command or target behavior:
- [exact command and current failure output, or exact behavior that should become true]
- [if no current failure exists, say so explicitly]

In scope:
- [allowed file or directory]
- [allowed behavior/doc/check change]

Out of scope:
- Do not change unrelated files.
- Do not add new dependencies unless explicitly approved.
- Do not change public API behavior unless this lane requires it.
- Do not introduce auth, persistence, deployment, or external integrations unless this lane requires it.
- Do not use real personal, employer, customer, incident, or secret data.

Security constraints:
- Do not hardcode secrets.
- Do not log secrets, request bodies, response bodies, auth headers, cookies, or arbitrary headers.
- Treat all user-provided text as untrusted.
- Keep example data fake and obviously synthetic.
- Preserve least-privilege CI/security posture.

Required implementation approach:
- Keep the diff small and reviewable.
- Prefer boring, explicit code over clever abstractions.
- Add or update meaningful tests when behavior changes.
- If the lane changes middleware, logging, authorization, validation, rate limiting, or another cross-cutting control, include non-happy-path tests such as 404s, handled errors, unhandled 500s, blocked requests, and privacy-sensitive failures.
- If the lane changes Dockerfile, Compose, container runtime config, or ignore files, prefer tests that parse/normalize config semantics instead of raw substring checks; prove localhost-only bindings, final non-root runtime user, no Docker socket/privileged/host networking, and any intended hardening controls.
- For docs-only changes, update links/checklists affected by the docs.
- If you find a pre-existing issue outside scope, report it instead of fixing it silently.

Required validation:
Use the repository's known tool environment before running checks. For this repo, activate the out-of-repo venv if it exists:

. /tmp/<repo-name>-venv/bin/activate

Run the strongest practical commands for this lane. Default for this repo:

make all

If a command cannot run, explain the exact error and whether it is project risk or environment/tooling risk. If a tool is missing, first confirm whether the repo has a documented virtualenv or install step before classifying the failure.

Final response format:
1. Summary of changes
2. Files changed
3. Tests/checks run with exact results
4. Security considerations
5. Assumptions
6. Residual risks or follow-up items
```
