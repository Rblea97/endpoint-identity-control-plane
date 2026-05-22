# Production-Readiness Checklist

## Scope

- [ ] Project purpose and non-goals are documented.
- [ ] Threat model or security assumptions are documented for production-like use.
- [ ] Real sensitive data is not used in tests, fixtures, examples, or prompts.

## Code quality

- [ ] Functions are focused and readable.
- [ ] No unrelated changes are mixed into the diff.
- [ ] Dependencies are justified.
- [ ] Public interfaces are documented or intentionally private.

## Verification

- [ ] `make lint` passes.
- [ ] `make format-check` passes.
- [ ] `make typecheck` passes.
- [ ] `make test` passes.
- [ ] `make security` is run and findings are triaged.

## Security

- [ ] No hardcoded secrets.
- [ ] External inputs are validated.
- [ ] Errors do not leak sensitive internals.
- [ ] Logs avoid secrets and sensitive bodies.
- [ ] CI permissions are least-privilege.
- [ ] Dependency/security findings are documented as fixed, accepted, or environment-only.

## Operations

- [ ] Configuration is documented.
- [ ] Startup command is documented.
- [ ] Rollback path is documented for deployment-like changes.
- [ ] Residual risks are listed.

## AI governance

- [ ] Codex implementation was narrow-scoped.
- [ ] Hermes performed spec-compliance review.
- [ ] Hermes performed code/test-quality review.
- [ ] Validation commands were actually run, not assumed.
- [ ] Lessons learned were added to AGENTS.md, a skill, or a checklist if reusable.
