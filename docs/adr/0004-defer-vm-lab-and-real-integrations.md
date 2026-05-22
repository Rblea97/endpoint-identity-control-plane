# ADR-0004: Defer VM Lab and Real Enterprise Integrations

## Status

Accepted

## Context

The project is IT-focused and references endpoint administration, Active Directory-style identity concepts, SCCM/MECM-style imaging, Intune-style compliance, Entra-style identity hygiene, and Defender-style endpoint security review. A natural question is whether the project should require virtual machines or live Microsoft integrations.

A VM/domain/SCCM lab can be educational, but it would make the main portfolio project heavier, slower to run, harder for reviewers to reproduce, and more likely to create data-handling mistakes. Real integrations would also require credentials, tenants, permission decisions, and strict publication controls.

## Decision

Do not require virtual machines or real enterprise integrations for the main MVP.

The main project runs as a local FastAPI app using synthetic demo inventory. VM labs, Microsoft Graph import simulators, Intune/Entra/SCCM/MECM mappings, or hosted live demos may be added later as optional, separately scoped extensions.

## Considered options

- VM-free FastAPI backend with synthetic data.
- Full local AD/domain lab with Windows Server and Windows client VMs.
- SCCM/MECM or Intune lab integration.
- Microsoft Graph integration with a demo tenant.
- Hosted public demo first.

## Rationale

A VM-free backend is the best first milestone for a public portfolio artifact. It is easy to run, test, inspect, and document. It still demonstrates endpoint and identity reasoning while avoiding licensing, resource, reproducibility, and data-safety problems.

VM and real-integration work can be valuable later, but only after the core system, documentation, and public-readiness controls are stable.

## Consequences

### Positive

- Lower setup burden for hiring managers and reviewers.
- No need for Windows Server, client VMs, Microsoft tenant credentials, or licenses.
- Safer publication path with synthetic-only data.
- Faster iteration on tests, docs, and API behavior.

### Negative / tradeoffs

- The MVP does not prove hands-on VM domain administration.
- The MVP does not prove live Microsoft Graph, Intune, Entra ID, SCCM/MECM, Defender, or AD integration.
- Some IT reviewers may ask how the simulated fields map to real tools; docs should answer that honestly.

## Revisit criteria

Revisit after the backend MVP, public docs, and file hygiene pass are complete. Good follow-up options include a synthetic import simulator, a diagram mapping fields to real-world systems, a small dashboard, a hosted demo, or a separate optional homelab appendix.
