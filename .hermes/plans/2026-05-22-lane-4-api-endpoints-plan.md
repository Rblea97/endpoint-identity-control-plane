# Lane 4 API Endpoints Implementation Plan

Goal: expose the synthetic inventory, findings, and risk report through behavior-tested FastAPI endpoints.

Scope:

- Add inventory endpoints: `GET /users`, `GET /devices`, `GET /groups`.
- Add security/risk endpoints: `GET /findings`, `GET /risk-report`.
- Keep data source synthetic and local only.
- Use a deterministic demo `as_of` timestamp for stable API examples.
- Do not add dashboard, persistence, auth, or external integrations.

Files:

- Modify: `src/endpoint_identity_control_plane/app.py`
- Create: `tests/test_api_endpoints.py`
- Create: `.hermes/checklists/2026-05-22-lane-4-validation.md`

Acceptance:

- Endpoints are exercised through FastAPI `TestClient`.
- Responses include `synthetic-demo-data-only` where relevant.
- `/risk-report` returns findings, severity counts, category counts, and top risky assets.
- `make all` passes or findings are classified.
