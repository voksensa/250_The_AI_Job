FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all source files first
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install Python dependencies (non-editable for production)
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run application
CMD ["uvicorn", "agent_runtime.main:app", "--host", "0.0.0.0", "--port", "8002"]
