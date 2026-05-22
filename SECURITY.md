# Security Policy

## Supported scope

This repository is treated as a private sandbox or portfolio project unless explicitly documented otherwise.

## Secret handling

- Do not commit secrets, API keys, passwords, tokens, private keys, or real sensitive data.
- Use environment variables or local `.env` files excluded by `.gitignore`.
- If a secret is exposed, rotate it immediately and document the incident.

## Security review expectations

Before publishing or production-like use, verify:

- Input validation at external boundaries.
- No hardcoded secrets or sensitive sample data.
- Dependency scan reviewed.
- Static analysis findings reviewed.
- Least-privilege CI permissions.
- Logging avoids secrets and sensitive request bodies.
- Residual risks are documented.

## Reporting

For private sandbox work, report issues directly to the repository owner. Do not include live secrets in issue text, commits, or chat transcripts.
