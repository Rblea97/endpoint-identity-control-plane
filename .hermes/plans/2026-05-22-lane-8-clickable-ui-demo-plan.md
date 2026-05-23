# Lane 8 Clickable UI Demo / GitHub Pages Plan

> **For Hermes:** Build a static, public-safe UI artifact that can be deployed to GitHub Pages only after Richie explicitly approves deployment/public exposure.

**Goal:** Add a clickable browser demo so reviewers can interact with endpoint/identity scenarios without cloning the repo or running FastAPI locally.

**Architecture:** Generate a static JSON bundle from the existing synthetic inventory, deterministic risk engine, and operations scenarios. Serve that bundle through a vanilla HTML/CSS/JavaScript dashboard under `site/`. Add local validation tests and docs. Prepare a manual GitHub Pages workflow but do not trigger public deployment without explicit approval.

**Tech Stack:** Python 3.11 exporter, existing Pydantic/risk/operations modules, vanilla HTML/CSS/JS, GitHub Pages manual workflow.

---

## Scope

In scope:

1. `scripts/export_static_demo.py` to build `site/demo-data.json` from committed synthetic data.
2. `site/index.html`, `site/styles.css`, and `site/app.js` for a clickable dashboard.
3. Tests that validate exported demo structure and required static assets.
4. README docs explaining local static preview and future Pages link.
5. Manual `workflow_dispatch` Pages workflow, pending explicit deployment approval.

Out of scope:

1. Making the repo public.
2. Triggering GitHub Pages deployment without approval.
3. Real Microsoft integrations.
4. Backend hosting, auth, database, or secrets.

## UI behavior

The dashboard should let a reviewer:

1. Click a scenario: failed imaging, disabled user assignment, privileged missing MFA, endpoint compliance queue.
2. See affected assets, findings, technician actions, and verification steps.
3. Click devices to see endpoint details and findings.
4. Click findings to see evidence and remediation.
5. Understand in under 60 seconds how the project maps to endpoint/identity IT work.

## Validation

Run:

```bash
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python scripts/export_static_demo.py
python -m pytest tests/test_static_demo.py -q
python -m http.server 4173 --directory site
make all
```

Then visually inspect `http://127.0.0.1:4173/`.
