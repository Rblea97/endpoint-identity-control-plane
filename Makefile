PYTHON ?= python3
PYTEST ?= pytest
PIP_AUDIT_PYTHON ?= $(shell command -v python3)

.PHONY: install-dev test lint lint-src-strict format-check typecheck security security-advisory security-blocking public-release-check all

install-dev:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest tests -q

lint:
	$(PYTHON) -m ruff check src tests

lint-src-strict:
	$(PYTHON) -m ruff check src --select D,ANN,N,PL,ARG,SIM,C4,RET,TRY --preview

format-check:
	$(PYTHON) -m ruff format --check src tests

typecheck:
	$(PYTHON) -m mypy src tests

security-advisory:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks detect --source . --no-git --redact; \
	else \
		echo "WARN: gitleaks not installed; skipping advisory secret scan"; \
	fi
	$(PYTHON) -m bandit -q -r src
	@PIPAPI_PYTHON_LOCATION="$(PIP_AUDIT_PYTHON)" $(PYTHON) -m pip_audit || echo "WARN: pip-audit findings require triage before public release"

security-blocking:
	@command -v gitleaks >/dev/null 2>&1 || (echo "ERROR: gitleaks is required for blocking release scans" && exit 1)
	gitleaks detect --source . --no-git --redact
	$(PYTHON) -m bandit -q -r src
	PIPAPI_PYTHON_LOCATION="$(PIP_AUDIT_PYTHON)" $(PYTHON) -m pip_audit

security: security-advisory

all: lint lint-src-strict format-check typecheck test security-advisory

public-release-check: lint lint-src-strict format-check typecheck test security-blocking
