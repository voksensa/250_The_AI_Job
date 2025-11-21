# TASK-003 Production Toggle MVP - End-to-End Workflow

## Metadata

- **Task ID**: TASK-003_production-toggle-mvp
- **Epic**: E001 – Foundation
- **Phase**: Phase 1 – MVP
- **Owner**: Developer
- **Status**: Done
- **Created**: 2025-11-21
- **Target Gates**: G5 (Tests), G6 (Builds), G10 (Owner can use it)
- **Related Decisions**:
  - [D-004] LangGraph 1.0.3
  - [D-001] Next.js 16
- **Inputs**:
  - [COMPLETE_ARCHITECTURE_SPEC.md](../../research/COMPLETE_ARCHITECTURE_SPEC.md)
  - [VISION.md](../../VISION.md)

## Problem Statement

Phase 1 goal: Prove that "Production Toggle" (Killer Feature #1) can work end-to-end. We need a minimal but complete workflow where Owner can submit a task via UI, and the system processes it using LangGraph orchestration.

This is the foundation for all subsequent Production Toggle features (quality gates, testing, etc.).

## Constraints

From CLAUDE.md Rule 1: **Phase A + Phase B Together**
- Must deliver BOTH backend capability AND frontend UI
- Owner must be able to SEE and USE the feature
- No backend-only deliverables

From VISION.md:
- Simple, magical UX for non-technical founders
- Real production code (no stubs)

## Plan

### Phase A (Backend)

1. **LangGraph Workflow** (`apps/agent-runtime/src/agent_runtime/graph.py`)
   - Define 3 nodes: `planner`, `coder`, `responder`
   - Use LangGraph StateGraph
   - Postgres checkpointer for persistence
   
2. **FastAPI Endpoint** (`apps/agent-runtime/src/agent_runtime/api/routes.py`)
   - `POST /api/tasks` - Submit new task
   - `GET /api/tasks/{task_id}` - Get task status
   - Request: `{ "description": "user task" }`
   - Response: `{ "task_id": "uuid", "status": "processing" }`

3. **State Schema** (`apps/agent-runtime/src/agent_runtime/types.py`)
   - TypedDict for AgentState
   - Fields: task, plan, code, status

### Phase B (Frontend)

1. **Task Submission Form** (`apps/web/src/app/page.tsx`)
   - Textarea for task description
   - "Submit Task" button
   - Display task ID + status response

2. **API Client** (`apps/web/src/lib/api.ts`)
   - `submitTask(description: string)` function
   - Fetch to `http://localhost:8002/api/tasks`

## Acceptance Criteria

**Backend (Phase A)**:
- [ ] `graph.py` with 3-node LangGraph workflow
- [ ] `POST /api/tasks` endpoint functional
- [ ] `GET /api/tasks/{task_id}` endpoint functional
- [ ] Postgres checkpointer configured
- [ ] Unit tests for workflow nodes

**Frontend (Phase B)**:
- [ ] Form on homepage with textarea + button
- [ ] API client submits to backend
- [ ] Response displayed to user

**Owner Validation (≤20 min)**:
- [ ] Open http://localhost:3030
- [ ] Enter task: "Create a hello world app"
- [ ] Click "Submit Task"
- [ ] See task ID + status returned

**Quality Gates**:
- [ ] G5: Tests written and passing
- [ ] G6: `docker-compose up` builds successfully
- [ ] G10: Owner can use it in browser

**Documentation**:
- [ ] All changes committed to Git
- [ ] Session log created in `docs/state/SESSIONS/`

## Notes / Links

This is the **first feature** of Phase 1. Success criteria: Owner can submit a task and see it processing. Actual code generation quality is secondary - focus on plumbing.

**Time Box**: 2-3 hours for both phases.
