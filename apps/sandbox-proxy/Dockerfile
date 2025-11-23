FROM python:3.11-slim

WORKDIR /app

# Install hatch to build the project
RUN pip install hatch

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY tests/ tests/

# Install dependencies and the project itself
RUN pip install .

# Create workspace directory
RUN mkdir -p /workspace && chmod 777 /workspace

# Expose port
EXPOSE 3001

# Run application
CMD ["uvicorn", "sandbox_proxy.main:app", "--host", "0.0.0.0", "--port", "3001"]
