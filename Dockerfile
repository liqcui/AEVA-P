# AEVA v2.0 Docker Image
# Multi-stage build for optimized production image

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-prod.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Install production libraries (optional, will use fallback if not available)
RUN pip install --no-cache-dir --user \
    adversarial-robustness-toolbox \
    great_expectations \
    statsmodels \
    streamlit \
    plotly \
    || echo "Some production libraries failed to install, fallback will be used"

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY aeva/ ./aeva/
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY config/ ./config/
COPY setup.py README.md LICENSE ./

# Install AEVA
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/results /app/data /app/logs

# Set Python path
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import aeva; print('OK')" || exit 1

# Default command: show help
CMD ["python", "-m", "aeva", "--help"]
