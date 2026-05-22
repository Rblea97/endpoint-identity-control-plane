# Development Guide

## Setup

```bash
python3 -m venv /tmp/endpoint-identity-control-plane-venv
. /tmp/endpoint-identity-control-plane-venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

Prefer an out-of-repo virtual environment for cleaner dependency and SBOM scans.

## Common commands

```bash
make lint
make format-check
make typecheck
make test
make security          # advisory local security scan
make all               # default local gate
make public-release-check  # blocking gate before public publication
```

Use `docs/change-management.md` before non-trivial changes and `docs/publication-runbook.md` before public release or publishing.

## Configuration

Keep `.env.example` aligned with every supported environment variable.
Do not commit real secrets.
