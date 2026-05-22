# ADR-0002: Use Synthetic Demo Data Only

## Status

Accepted

## Context

The project is intended for portfolio review and eventual public GitHub visibility. The domain is endpoint and identity operations, which can involve sensitive enterprise data: usernames, hostnames, group names, tenant IDs, device compliance state, patch posture, security findings, logs, screenshots, and administrative exports.

Using real employer, tenant, AD, SCCM/MECM, Intune, Entra ID, Defender, SIEM, or endpoint data would create privacy, security, and professional-risk problems.

## Decision

Use only committed synthetic demo data for the MVP. All demo inventory and sample responses must be safe for public review and classified as:

```text
synthetic-demo-data-only
```

No real employer, tenant, user, device, hostname, group, credential, screenshot, log, ticket, incident, or export data may be committed.

## Considered options

- Synthetic JSON fixture committed to the repo.
- Real exports from a lab tenant or domain.
- Real employer exports with redaction.
- Generated data at runtime.

## Rationale

A committed synthetic fixture is simple, deterministic, reviewable, and testable. It lets reviewers run the project quickly without needing a tenant, VM, Microsoft license, or secrets.

Real exports are inappropriate for a public portfolio project. Even redacted exports can leak structure, naming conventions, timing, organizational context, or operational details. Runtime-generated data would reduce fixture-review risk but would make examples and tests less stable unless generation is carefully seeded.

## Consequences

### Positive

- Safe default for eventual public release.
- Stable tests and documentation examples.
- No need for tenant credentials, VM lab setup, or employer data.
- Clear reviewer confidence that the project was designed for safe publication.

### Negative / tradeoffs

- Demo data is simplified compared with real endpoint-management and identity systems.
- The MVP does not prove live Microsoft Graph, AD, SCCM/MECM, Intune, Entra ID, or Defender integration.
- Public reviewers must evaluate the domain model and rules as a simulation, not as production telemetry.

## Revisit criteria

Revisit if a future lane adds an import simulator, hosted demo, or real integration. Any such lane must preserve public safety by using synthetic exports, placeholders, least-privilege credentials, and explicit redaction rules. Real employer data remains out of scope.
