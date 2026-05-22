# API Documentation

The API is read-only in the current MVP. It serves committed synthetic demo inventory and deterministic risk results.

All examples assume the app is running locally:

```bash
uvicorn endpoint_identity_control_plane.app:app --reload
```

Generated docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Data classification

The project uses only fake demo data. API metadata and risk reports identify this as:

```text
synthetic-demo-data-only
```

Do not add real employer, tenant, user, device, group, hostname, screenshot, credential, or export data.

## Endpoints

### `GET /health`

Purpose: return a minimal smoke-check response for local runs and CI.

Example:

```bash
curl --silent http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

### `GET /version`

Purpose: return app metadata and data classification.

Example:

```bash
curl --silent http://127.0.0.1:8000/version
```

Response:

```json
{
  "name": "endpoint-identity-control-plane",
  "version": "0.1.0",
  "data_classification": "synthetic-demo-data-only"
}
```

### `GET /users`

Purpose: return synthetic identity records.

Example:

```bash
curl --silent http://127.0.0.1:8000/users
```

Response shape:

```json
[
  {
    "id": "user-001",
    "username": "alex.rivera@example.example",
    "display_name": "Alex Rivera Demo",
    "department": "Demo Service Desk",
    "enabled": true,
    "last_login_at": "2026-05-18T14:20:00Z",
    "mfa_enabled": true,
    "privileged_groups": [],
    "assigned_device_ids": ["device-001"]
  }
]
```

### `GET /devices`

Purpose: return synthetic endpoint records.

Example:

```bash
curl --silent http://127.0.0.1:8000/devices
```

Response shape:

```json
[
  {
    "id": "device-001",
    "hostname": "DEMO-WIN11-001",
    "assigned_user_id": "user-001",
    "os_name": "Windows 11 Enterprise",
    "os_version": "23H2",
    "last_checkin_at": "2026-05-21T13:10:00Z",
    "patch_status": "current",
    "encryption_enabled": true,
    "local_admin_count": 1,
    "compliance_state": "compliant",
    "imaging_state": "complete"
  }
]
```

### `GET /groups`

Purpose: return synthetic identity group records.

Example:

```bash
curl --silent http://127.0.0.1:8000/groups
```

Response shape:

```json
[
  {
    "id": "group-001",
    "name": "Demo Endpoint Readers",
    "privilege_level": "standard",
    "member_user_ids": ["user-001", "user-003"]
  }
]
```

### `GET /findings`

Purpose: return deterministic endpoint and identity findings for the synthetic inventory.

Example:

```bash
curl --silent http://127.0.0.1:8000/findings
```

Response shape:

```json
[
  {
    "id": "identity-privileged-user-missing-mfa-user-002",
    "severity": "high",
    "category": "identity",
    "title": "Privileged user does not have MFA enabled",
    "asset_type": "user",
    "asset_id": "user-002",
    "evidence": {
      "username": "jamie.chen@example.example",
      "privileged_group_count": 1,
      "mfa_enabled": false
    },
    "recommendation": "Require MFA for privileged endpoint or identity access.",
    "control_mapping": "Identity hygiene: privileged access protection"
  }
]
```

### `GET /risk-report`

Purpose: return a summarized deterministic report with counts, top risky assets, and findings.

Example:

```bash
curl --silent http://127.0.0.1:8000/risk-report
```

Shortened response:

```json
{
  "generated_at": "2026-05-22T12:00:00Z",
  "data_classification": "synthetic-demo-data-only",
  "finding_counts_by_severity": {
    "high": 9,
    "medium": 4
  },
  "finding_counts_by_category": {
    "lifecycle": 1,
    "imaging": 2,
    "identity": 2,
    "endpoint": 5,
    "compliance": 3
  },
  "top_risky_assets": [
    {
      "asset_type": "device",
      "asset_id": "device-003",
      "finding_count": 6,
      "highest_severity": "high"
    }
  ],
  "findings": []
}
```

The actual `findings` array is populated in the live response; it is shortened here to keep the docs readable.

## Error behavior

The current implemented endpoints are read-only and do not accept request bodies. FastAPI still returns framework-standard errors for unsupported methods or malformed paths.

Expected classes of errors as the project grows:

- `404`: route not found.
- `405`: method not allowed.
- `422`: validation error if future request parameters or bodies are added.
- `500`: unexpected server error; responses should not leak secrets or private internals.

## Current API limitations

- No authentication or authorization.
- No write endpoints.
- No pagination or filtering.
- No live Microsoft integration.
- No persistence or historical trend storage.
- No production-grade rate limiting, logging, or audit trail.
