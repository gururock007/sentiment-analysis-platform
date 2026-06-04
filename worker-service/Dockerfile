# --- Build Stage ---
FROM astral/uv:python3.14-trixie-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 

COPY application/pyproject.toml application/uv.lock ./

# Install deps first (better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY application/ ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev 

# --- Production Stage ---
FROM python:3.14-slim

WORKDIR /app

# Proper user creation for Debian
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy virtualenv + app
COPY --chown=appuser:appgroup --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appgroup application/ ./

USER appuser

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["python", "main.py"]