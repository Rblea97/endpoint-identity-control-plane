# API Documentation

Document public endpoints here in addition to generated OpenAPI docs.

## OpenAPI

When running locally:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Endpoint template

### `METHOD /path`

Purpose: Replace this with what the endpoint does.

Request body:

```json
{}
```

Success response:

```json
{}
```

Error responses:

- `400` / `422`: validation or malformed input.
- `401` / `403`: authentication or authorization failure, when applicable.
- `429`: rate limit, when applicable.
- `500`: unexpected server error; do not leak internals.
