# Agent Runtime

LangGraph-based runtime service for Your First Engineer.

## Features

- LangGraph 1.0.3 native patterns (StateGraph, astream_events v2)
- PostgreSQL-based checkpointer for persistence
- FastAPI REST API
- Production-ready Docker image

## Local Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run server
uvicorn agent_runtime.main:app --reload --port 8002
```

## Docker

```bash
docker build -t yfe-agent-runtime .
docker run -p 8002:8002 --env-file .env yfe-agent-runtime
```

## Health Check

```bash
curl http://localhost:8002/health
```
