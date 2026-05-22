# Architecture Decision Records

This directory records project decisions that affect architecture, public-safety posture, and reviewer expectations.

## ADR index

- [ADR-0001: Use FastAPI](0001-use-fastapi.md)
- [ADR-0002: Use synthetic demo data only](0002-use-synthetic-demo-data.md)
- [ADR-0003: Use deterministic risk rules for the MVP](0003-use-deterministic-risk-rules.md)
- [ADR-0004: Defer VM lab and real enterprise integrations](0004-defer-vm-lab-and-real-integrations.md)

## Maintenance rules

- Add a new ADR when a major architecture, security, data-handling, or deployment decision changes.
- Mark older decisions as superseded instead of silently deleting history.
- Do not include real employer, tenant, user, device, hostname, export, credential, or private operational data.
- Distinguish implemented controls from deferred production controls.
