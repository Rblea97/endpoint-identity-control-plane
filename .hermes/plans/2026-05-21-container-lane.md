# Container lane rehearsal plan

## Purpose

Rehearse container packaging for the secure Python/FastAPI scaffold in a private repo before any public release. This lane tests whether Hermes/Codex can add runtime packaging, least-privilege container defaults, local Compose ergonomics, documentation, and container-specific security gates without widening scope into cloud deployment.

## Scope

Implement a local/private container lane with:

- A `Dockerfile` for the FastAPI application.
- A `.dockerignore` that prevents caches, virtualenvs, git metadata, local databases, scan reports, and secrets from entering the build context.
- A `compose.yml` or `docker-compose.yml` that runs the API locally.
- Local-only port binding, preferably `127.0.0.1:8000:8000`.
- Non-root runtime user in the image.
- No Docker socket mount, privileged mode, broad capabilities, or host filesystem mounts.
- Health verification via the existing `/health` endpoint.
- Documentation for build/run/scan/cleanup commands.
- Tests or static checks proving the critical container configuration expectations.

## Non-goals

- No cloud deployment.
- No Kubernetes.
- No registry push.
- No production secrets.
- No public repository publication.
- No real user, employer, customer, or incident data.
- No database container unless required by the app; this scaffold currently only needs the API container.

## Security requirements

- Run the app as a non-root user.
- Bind Compose service to localhost only.
- Do not mount `/var/run/docker.sock`.
- Do not use `privileged: true`.
- Do not copy `.env`, `.git`, virtualenvs, caches, `.hermes/reports`, local DB files, or generated metadata into the image build context.
- Use fake/local example values only.
- Keep the final image minimal and boring; prefer clear reproducibility over clever optimization.

## TDD/static verification plan

Before implementation, add tests that fail because container files do not exist yet. Tests should verify:

- `Dockerfile` exists.
- `.dockerignore` exists and excludes high-risk/generated paths.
- Compose file exists.
- Compose port binding is localhost-only.
- Compose does not use privileged mode or Docker socket mounts.
- Dockerfile creates/uses a non-root runtime user.
- Dockerfile starts uvicorn for `endpoint_identity_control_plane.app:app` on `0.0.0.0:8000`.

## Runtime verification plan

After implementation:

```bash
make PYTHON=/tmp/endpoint-identity-control-plane-venv/bin/python PIP_AUDIT_PYTHON=/tmp/endpoint-identity-control-plane-venv/bin/python public-release-check
actionlint .github/workflows/*.yml
hadolint Dockerfile
dockerfilelint Dockerfile
docker compose config
docker compose build api
docker compose up -d api
curl --fail --silent http://127.0.0.1:8000/health
docker compose exec -T api id
docker compose down -v
trivy fs .
trivy image endpoint-identity-control-plane-api
syft .
grype dir:.
hermes-publication-gate --repo .
hermes-sec-scan --repo .
```

If a tool reports environment or database update noise, classify the finding with evidence rather than suppressing it blindly.

## Acceptance criteria

- Tests prove critical container configuration.
- Local app still passes all Python quality/security gates.
- Dockerfile and Compose lint/config pass or findings are fixed/classified.
- Image builds successfully.
- Containerized API responds on localhost `/health`.
- Runtime user is non-root when inspected inside the container.
- Compose cleanup leaves no running project containers.
- Security scans pass or findings are classified with evidence.
- Private PR is opened and left for Richie final review.
