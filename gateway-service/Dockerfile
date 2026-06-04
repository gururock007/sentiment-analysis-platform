# --- Build Stage --- 
FROM astral/uv:python3.14-alpine AS builder

WORKDIR /app

# Pre-compile Python source files to bytecode for faster container startup
ENV UV_COMPILE_BYTECODE=1 

COPY application/pyproject.toml application/uv.lock ./

# Install third-party dependencies first to maximize layer caching
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

COPY application/ ./

# Sync again to build and link the project source code into the virtual environment
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev 

# --- Production Stage ---
FROM python:3.14-alpine

WORKDIR /app

# Create a minimal, non-privileged system user for security isolation
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy assets and set non-root ownership in a single step to optimize layer size
COPY --chown=appuser:appgroup --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appgroup application/ ./

USER appuser

# Expose virtual environment binaries and configure application import paths
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]