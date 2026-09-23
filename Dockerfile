# Multi-stage Dockerfile for Sales Analytics application

# Stage 1: Build wheel artifact
FROM python:3.12-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir --upgrade pip build wheel setuptools

COPY pyproject.toml setup.py README.md ./
COPY src/ ./src/

RUN python -m build --wheel --outdir /build/dist

# Stage 2: Minimal runtime image
FROM python:3.12-slim AS runtime

# Create dedicated non-root user for security
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/bash -m appuser

WORKDIR /app

# Copy built wheel from builder stage and install
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

# Copy sample data
COPY --chown=appuser:appuser data/ /app/data/

USER appuser

ENTRYPOINT ["sales"]
CMD ["-i", "/app/data/sample_sales.csv"]
