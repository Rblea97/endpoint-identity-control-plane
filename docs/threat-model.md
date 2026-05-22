# Threat Model

## Assets

- Application source code.
- Runtime configuration and secrets.
- Request/response data.
- Logs and audit records.
- CI/CD credentials and artifacts.

## Trust boundaries

- External client to API boundary.
- API to persistence boundary, if persistence exists.
- CI/CD to deployment boundary, if deployment exists.

## Threats to consider

- Invalid or malicious input.
- Sensitive data exposure in logs/errors/docs/tests.
- Hardcoded secrets.
- Dependency compromise.
- Over-permissive CI/CD tokens.
- Authentication or authorization bypass, when auth exists.

## Controls

Map implemented controls to each threat. Mark missing controls as known limitations or roadmap items.

## Residual risk

Document remaining risk after controls are applied.
