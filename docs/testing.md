# Testing Strategy

## Test categories

- Unit tests for pure domain logic.
- API tests for routes, validation, and error responses.
- Security-focused regression tests for unsafe logging, invalid input, authorization, and rate limiting when applicable.

## Expectations

- Tests should prove behavior, not just increase coverage.
- Negative paths matter: invalid payloads, unauthorized requests, missing routes, handled errors, unhandled 500s, rate limits, and malformed input.
- Middleware and cross-cutting controls must be tested on paths where the application does not return a normal 200 response.
- Avoid real sensitive data in fixtures and examples.
- Do not require docstrings on every test; prefer clear test names.


## Validation evidence

For every meaningful lane, record exact commands and results using `.hermes/checklists/validation-log-template.md`. Public-facing changes should include security/dependency scan classification and CI status before merge or publication.

## Webhook rehearsal notes

Tiny documentation-only pull requests can be used to rehearse the GitHub webhook and Tier 2 Kanban triage flow. These rehearsals should verify event delivery, Kanban deduplication, and read-only guardrails without changing application behavior or introducing external data.

Post-hardening rehearsals should also confirm capture-only Kanban cards remain scheduled until explicitly approved, so webhook delivery never implies worker dispatch.
