# Security Posture

## Scope

Describe what the project protects and what is explicitly out of scope.

## Security goals

- Validate untrusted input at service boundaries.
- Avoid logging secrets or sensitive request bodies.
- Keep errors safe and non-revealing.
- Use least privilege for CI, containers, credentials, and services.
- Keep dependency and secret scanning part of the normal gate.

## Implemented controls

Replace with current controls, such as validation, logging, auth, rate limiting, and scans.

## Known limitations

List limitations honestly. Do not imply production readiness before controls exist.

## Finding classification

Classify security findings as one of:

- fixed;
- accepted risk with justification;
- false positive with justification;
- environment/tooling-only issue;
- deferred with a tracked follow-up.
