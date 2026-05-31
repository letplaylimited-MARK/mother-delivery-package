FROM python:3.12-slim

LABEL maintainer="Ghost Hub Team <team@ghosthub.dev>"
LABEL version="1.0.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GHOST_HUB_VERSION=1.0.0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY 03_SDK与集成/03_企业SDK包/GhostHub_SDK/ ./

RUN pip install --no-cache-dir -e ".[all]" || pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

EXPOSE 8080 8883 5672

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import ghost_hub_sdk; print('ok')" || exit 1

CMD ["uvicorn", "ghost_hub_sdk.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
