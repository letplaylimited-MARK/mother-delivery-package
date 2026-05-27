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

COPY pyproject.toml README.md LICENSE ./

RUN pip install --no-cache-dir ghost-hub-sdk==${GHOST_HUB_VERSION}

RUN pip install --no-cache-dir -e ".[all]" || true

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8080 8883 5672

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import ghost_hub_sdk; print('ok')" || exit 1

CMD ["python", "-c", "from ghost_hub_sdk.api.main import app; app.run(host='0.0.0.0', port=8080)"]
