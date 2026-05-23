# Lane 8 Validation Checklist — Clickable Static UI Demo

Date: 2026-05-23
Branch: `feat/clickable-pages-demo`

## Scope validated

- Added static UI under `site/`:
  - `site/index.html`
  - `site/styles.css`
  - `site/app.js`
  - `site/demo-data.json`
- Added `scripts/export_static_demo.py` to generate the static JSON payload from existing synthetic inventory, risk report, and operations scenarios.
- Added manual-only GitHub Pages workflow: `.github/workflows/pages.yml`.
- Added tests for static payload shape, static assets, and committed JSON freshness.
- Updated README with local browser preview instructions.

## Important deployment boundary

The GitHub Pages workflow uses `workflow_dispatch` only. It does not deploy automatically on push or merge. Public deployment still requires Richie’s explicit approval because a Pages site is a published browser-accessible artifact.

## Automated validation

Commands run:

```bash
python scripts/export_static_demo.py
python -m pytest tests/test_static_demo.py -q
make all
actionlint .github/workflows/*.yml
```

Results:

- Static exporter wrote `site/demo-data.json` successfully.
- Static demo tests: `3 passed`.
- Full test suite: `34 passed`.
- Ruff normal lint: passed.
- Strict Ruff source lint: passed.
- Ruff format check: passed.
- mypy: passed.
- gitleaks: no leaks found.
- bandit: no known vulnerabilities.
- actionlint: passed.
- pip-audit advisory: local editable package is not on PyPI and cannot be audited as a package; no known third-party vulnerabilities reported.

## Browser validation

Served locally with:

```bash
python -m http.server 4173 --directory site
```

Opened:

```text
http://127.0.0.1:4173/
```

Observed:

- Hero loads with summary counts for devices, users, and findings.
- Scenario cards render.
- Scenario detail panel updates through JavaScript.
- Remediation queue renders top devices.
- Device detail panel renders endpoint ownership/compliance/imaging/patch findings.
- Findings section renders severity filters and finding cards.

## Public-safety notes

- Static payload is generated from committed synthetic fixture data only.
- No real tenant, employer, AD, SCCM/MECM, Intune, Entra, Defender, username, hostname, screenshot, credential, connection string, or export data was added.
- Repository remains private pending separate publication approval.
