# Operational Context: Navigation Guide

**Version**: 2.1 (Aligned with CONST_MERGE_PLAN)  
**Date**: 2025-11-23  
**Purpose**: Quick reference for where to read first and where things live.

---

## Start Here (Reading Order)

1. `constitution/VISION.md`
2. `constitution/STRATEGY.md`
3. `constitution/ROADMAP_SPEC.md`
4. `constitution/GOLDEN_RULES.md`
5. `constitution/ARCHITECTURAL_DECISIONS.md`
6. `constitution/EXECUTION_PROTOCOL_SPEC.md`
7. `constitution/STATE_MANAGEMENT.md` → then `docs/state/INDEX.md`
8. Finally, open your role manual (`AGENTS.md`, `VALIDATOR.md`, or `CLAUDE.md`) before doing anything.

---

## Document Hierarchy

```
constitution/
  VISION.md → STRATEGY.md → ROADMAP_SPEC.md
  GOLDEN_RULES.md → ARCHITECTURAL_DECISIONS.md
  EXECUTION_PROTOCOL_SPEC.md → STATE_MANAGEMENT.md
docs/state/
  INDEX.md (SSoT) → CURRENT_TASK.md → PROGRESS.md → BLOCKERS.md → DECISIONS_LOG.md
```

---

## Directory Structure (Monorepo)

```
/
├── constitution/              # Core specs and rules
├── docs/
│   ├── state/                 # Living state spine (INDEX, CURRENT_TASK, etc.)
│   └── research/              # Research briefs and specs
├── apps/
│   ├── web/                   # Owner console (Next.js 16, Tailwind CSS 4, shadcn/ui)
│   ├── agent-runtime/         # LangGraph/FastAPI runtime (/api/v1/... endpoints)
│   ├── agent-api/             # API-facing service layer
│   └── sandbox-manager/       # Sandbox orchestration
├── packages/                  # Shared packages (if any)
├── infra/                     # Infra-as-code and ops scripts
└── docker-compose.yml         # Orchestrates postgres, agent-runtime, owner-console
```

---

## Technology Stack

- **API pattern**: All HTTP/WebSocket routes use `/api/v1/...` and RFC 9457 error shape.
- **Backend (apps/agent-runtime/)**: FastAPI + LangGraph 1.0.3, PostgresSaver persistence, PostgreSQL + pgvector.
- **Frontend (apps/web/)**: Next.js 16 (App Router, TypeScript strict) with Tailwind CSS 4 and shadcn/ui.
- **Testing**: Pytest 9.x + coverage for backend; Vitest/Jest with coverage for frontend (target ≥85% on changed code per GOLDEN_RULES).
- **State**: LangGraph state is additive/versioned; no field removals or renames without migration.

---

## Service Ports (docker-compose)

| Service         | Port | Notes                                   |
|-----------------|------|-----------------------------------------|
| owner-console   | 3000 | Next.js UI (points to agent-runtime API)|
| agent-runtime   | 8002 | FastAPI + LangGraph backend             |
| postgres        | 5432 | Primary datastore (pgvector enabled)    |

---

## Common Commands

```bash
# Start services
docker-compose up -d

# Logs
docker-compose logs -f agent-runtime
docker-compose logs -f owner-console

# Health check (backend)
curl http://localhost:8002/health
```

Run lint/tests/coverage via Docker workflows per `constitution/EXECUTION_PROTOCOL_SPEC.md` (no local `uvicorn` or `npm run dev`).

---

## Environment Variables

Defined in `.env` (consumed by docker-compose):

```
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
DATABASE_URL=postgresql://yfe:yfe_dev_pass@postgres:5432/yfe_db
ENVIRONMENT=development
```

Add additional provider keys as needed; never hardcode secrets.

---

## Quick Links

- SSoT: `docs/state/INDEX.md`
- Current task: `docs/state/CURRENT_TASK.md`
- Evidence templates: `evidence/.template/`
- API spec: `openapi/yfe-api-v1.yaml`
