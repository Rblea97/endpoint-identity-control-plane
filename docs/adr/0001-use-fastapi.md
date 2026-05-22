# ADR-0001: Use FastAPI

## Status

Proposed

## Context

This project needs a Python API framework that supports typed request/response models, generated OpenAPI documentation, and testable route handlers.

## Decision

Use FastAPI for HTTP API projects unless a project-specific constraint requires another framework.

## Considered options

- FastAPI
- Flask
- Django / Django REST Framework

## Rationale

FastAPI aligns well with PEP 484 type hints, Pydantic validation, generated OpenAPI docs, and small service boundaries.

## Consequences

### Positive

- Strong request/response schema support.
- Good local developer experience.
- Generated `/docs`, `/redoc`, and `/openapi.json`.

### Negative / tradeoffs

- Requires care around async/sync boundaries.
- Does not provide Django-style batteries-included persistence/admin features.

## Revisit criteria

Revisit if the project needs a full-stack framework, complex admin UI, or framework-level features FastAPI does not provide.
