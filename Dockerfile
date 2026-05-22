FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser -D -h /home/appuser appuser

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir . \
    && rm -rf src/*.egg-info

USER appuser

EXPOSE 8000

CMD ["uvicorn", "endpoint_identity_control_plane.app:app", "--host", "0.0.0.0", "--port", "8000"]
