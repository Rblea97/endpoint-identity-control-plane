# Lane 3 Risk Engine Implementation Plan

Goal: implement deterministic endpoint and identity risk findings over the validated synthetic inventory.

Scope:

- Add a focused `risk.py` module.
- Keep all rule logic pure Python and independent of FastAPI.
- Do not add API endpoints yet.
- Do not add dependencies.
- Use a caller-provided `as_of` datetime so tests do not depend on the current date.

Files:

- Create: `src/endpoint_identity_control_plane/risk.py`
- Create: `tests/test_risk.py`
- Create: `.hermes/checklists/2026-05-22-lane-3-validation.md`

Rules to implement:

1. privileged user without MFA;
2. disabled user still assigned to device;
3. stale user login beyond 60 days;
4. stale device check-in beyond 30 days;
5. Windows 10 device treated as unsupported for demo timeline;
6. endpoint encryption disabled;
7. local administrator exposure above 1;
8. noncompliant endpoint;
9. failed or incomplete imaging state;
10. missing/unknown patch status.

Acceptance:

- Findings have stable IDs, severity, category, asset type/id, evidence, recommendation, and control mapping.
- Risk report summarizes counts and top risky assets.
- Behavior tests cover expected demo findings and no-date-flakiness.
- `make all` passes or findings are classified.
