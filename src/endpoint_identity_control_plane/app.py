"""Application entrypoint for the secure Python service template."""

from fastapi import FastAPI

app = FastAPI(title="Replace Me Secure Python Service")


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal health response for local and CI smoke checks."""
    return {"status": "ok"}
