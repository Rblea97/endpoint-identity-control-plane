# ADR-0001: Use FastAPI

## Status

Accepted

## Context

The project needs a small Python API framework for a local portfolio backend. The service should expose typed JSON responses, generate useful OpenAPI docs, support straightforward tests, and keep business logic separate from route handlers.

## Decision

Use FastAPI for the HTTP API layer.

## Considered options

- FastAPI.
- Flask.
- Django / Django REST Framework.
- CLI-only project with no HTTP API.

## Rationale

FastAPI fits the current project because it works naturally with Python type hints and Pydantic models. It provides generated Swagger UI, ReDoc, and OpenAPI JSON without a separate documentation framework. It also supports simple `TestClient` tests that exercise real HTTP route behavior.

Flask would also work, but it would require more manual schema and OpenAPI decisions. Django REST Framework would be heavier than the current MVP needs. CLI-only output would be easier to build but less useful as a portfolio artifact for backend/API and DevSecOps review.

## Consequences

### Positive

- Typed response models and clear route handlers.
- Generated local API docs at `/docs`, `/redoc`, and `/openapi.json`.
- Good testability with FastAPI `TestClient`.
- Clear path to a later dashboard or hosted demo.

### Negative / tradeoffs

- Requires care if async handlers, background tasks, or external clients are added later.
- Does not provide Django-style built-in persistence, admin UI, or user management.
- FastAPI alone does not provide production controls such as auth, rate limiting, deployment hardening, or observability.

## Revisit criteria

Revisit this decision if the project becomes a full-stack web app, needs a built-in admin interface, requires a different runtime language, or moves from local/demo API into a production-like multi-user service.
