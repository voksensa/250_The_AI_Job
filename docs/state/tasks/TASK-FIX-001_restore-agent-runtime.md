# TASK-FIX-001: Restore Agent Runtime Service to Working State

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL / BLOCKING**  
**Date**: 2025-11-21  
**Blocks**: Phase 1 MVP - Cannot proceed until service is functional  
**Estimated Effort**: 6-8 hours  

---

## Objective

Restore `apps/agent-runtime` to a **working, production-grade state** by implementing the missing `api/routes.py` and `graph.py` files using **ONLY native LangGraph 1.0.3 patterns** verified against official documentation via MCP tool.

**Non-Negotiable Requirements:**
1. **Production from Line 1** - No stubs, no TODOs, no placeholders
2. **Native over Custom** - All LangGraph patterns must be native (verified via MCP)
3. **Evidence-Based** - All implementation decisions must cite official docs
4. **Testable** - Service must start, pass health checks, and execute a real task end-to-end

---

## Context

**Audit Finding V-001**: `main.py` imports `from .api.routes import router as tasks_router` but the file does not exist. Service cannot start. This violates "production from line 1."

**Current State:**
- ✅ `main.py` exists with FastAPI skeleton
- ✅ Settings, CORS, health endpoint configured
- ❌ `api/` directory missing
- ❌ `routes.py` missing
- ❌ `graph.py` missing (LangGraph implementation)
- ❌ Service cannot run

**Required State:**
- ✅ Service starts successfully
- ✅ Health check returns 200 OK
- ✅ Can create and execute a task end-to-end
- ✅ Uses PostgresSaver for state (not MemorySaver)
- ✅ Uses native LangGraph streaming (astream, get_stream_writer)
- ✅ All code is lint-clean and type-safe

---

## Pre-Work (Research Phase)

### Step 1: Query Official LangGraph Documentation

**You MUST run these MCP queries and document the results:**

```python
# Query 1: LangGraph 1.0.3 basics
mcp0_SearchDocsByLangChain(query="langgraph 1.0.3 StateGraph basic example")

# Query 2: PostgreSQL checkpointer
mcp0_SearchDocsByLangChain(query="langgraph PostgresSaver checkpoint postgres setup")

# Query 3: Streaming events
mcp0_SearchDocsByLangChain(query="langgraph astream streaming custom events stream_mode")

# Query 4: Custom events with get_stream_writer
mcp0_SearchDocsByLangChain(query="langgraph get_stream_writer custom events tutorial")

# Query 5: Human-in-the-loop interrupts
mcp0_SearchDocsByLangChain(query="langgraph interrupt human approval Command")

# Query 6: FastAPI integration
mcp0_SearchDocsByLangChain(query="langgraph fastapi integration async streaming")
```

**Document findings in:**
`docs/state/SESSIONS/2025-11-21_dev_fix001-research.md`

**Include for each query:**
- Query text
- Key findings (code examples, patterns)
- Links to official docs
- How it applies to our implementation

---

## Implementation (Execution Phase)

### Part A: Create Directory Structure

```bash
cd apps/agent-runtime/src/agent_runtime
mkdir -p api
touch api/__init__.py
touch api/routes.py
touch graph.py
```

**Evidence**: Directory listing showing new files created.

---

### Part B: Implement `graph.py` (LangGraph Core)

**Requirements:**

1. **Use Native StateGraph Pattern**
   - Define state using TypedDict (not Pydantic BaseModel unless docs show it)
   - Reference: Your MCP Query 1 results

2. **Use PostgresSaver for Checkpointing**
   - Import: `from langgraph.checkpoint.postgres import PostgresSaver`
   - Connection string from `Settings.database_url`
   - Call `checkpointer.setup()` in graph initialization
   - Reference: Your MCP Query 2 results

3. **Implement At Least 2 Nodes**
   - `planner_node`: Takes task description, creates plan
   - `executor_node`: Executes plan (for Phase 0, can be simple)
   - Both must use real LLM calls (ChatAnthropic or ChatOpenAI from settings)

4. **Use Native Streaming**
   - Graph compiled with: `graph.compile(checkpointer=checkpointer)`
   - Execution via: `graph.astream(..., stream_mode=["updates", "custom"])`
   - Custom events via: `get_stream_writer()` inside nodes
   - Reference: Your MCP Query 3 & 4 results

5. **Type Safety**
   - All functions must have type hints
   - Must pass `mypy src/ --ignore-missing-imports`

**Code Structure:**

```python
# graph.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.config import get_stream_writer
# ... other imports from official docs

class AgentState(TypedDict):
    """State for the agent graph."""
    task: str
    plan: str | None
    result: str | None
    # Add fields as needed per official examples

async def planner_node(state: AgentState) -> dict:
    """Create a plan from task description."""
    # MUST use real LLM call (no mocks)
    # MUST emit custom event via get_stream_writer
    # Reference your MCP query results
    pass

async def executor_node(state: AgentState) -> dict:
    """Execute the plan."""
    # MUST use real LLM call or actual code execution
    # Reference your MCP query results
    pass

def create_graph(database_url: str, llm_api_key: str) -> ...:
    """Create and return compiled LangGraph."""
    # Initialize checkpointer
    checkpointer = PostgresSaver.from_conn_string(database_url)
    checkpointer.setup()  # Create tables if needed
    
    # Build graph using ONLY patterns from MCP queries
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)
    
    return workflow.compile(checkpointer=checkpointer)

# NOTE: This is a template. Your actual implementation MUST follow
# the exact patterns from your MCP query results. If the official docs
# show a different pattern, use that instead.
```

**Validation:**
- [ ] All imports resolve
- [ ] `mypy` passes
- [ ] `ruff check` passes
- [ ] Code matches patterns from MCP queries (document which query for each pattern)

---

### Part C: Implement `api/routes.py` (FastAPI Endpoints)

**Requirements:**

1. **POST /api/tasks Endpoint**
   - Accepts: `{"task": "description of what to build"}`
   - Returns: `{"task_id": "uuid", "status": "running"}`
   - Starts LangGraph execution in background via `BackgroundTasks`

2. **GET /api/tasks/{task_id} Endpoint**
   - Returns: Current state from PostgresSaver
   - Must query checkpointer for state, not in-memory cache

3. **WebSocket /api/tasks/{task_id}/stream Endpoint**
   - Streams LangGraph events in real-time
   - Uses `graph.astream()` with `stream_mode=["updates", "custom"]`
   - Reference: Your MCP Query 6 results

4. **Error Handling**
   - All endpoints must have try/except
   - Return proper HTTP status codes
   - Log errors (no silent failures)

**Code Structure:**

```python
# api/routes.py
from fastapi import APIRouter, BackgroundTasks, WebSocket
from pydantic import BaseModel
import uuid

from ..graph import create_graph
from ..main import settings

router = APIRouter()

# Initialize graph (singleton or per-request, based on MCP findings)
graph = create_graph(settings.database_url, settings.anthropic_api_key)

class TaskRequest(BaseModel):
    task: str

@router.post("/tasks")
async def create_task(request: TaskRequest, background: BackgroundTasks):
    """Create and start a new task."""
    task_id = str(uuid.uuid4())
    
    # Start graph execution in background
    # Use pattern from MCP Query 6 for FastAPI integration
    
    return {"task_id": task_id, "status": "running"}

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get current task state from checkpointer."""
    # Query PostgresSaver for state
    # Return structured response
    pass

@router.websocket("/tasks/{task_id}/stream")
async def stream_task(websocket: WebSocket, task_id: str):
    """Stream real-time task execution events."""
    await websocket.accept()
    
    # Use graph.astream with stream_mode per MCP Query 3 & 4
    
    pass

# NOTE: Actual implementation must follow MCP query results exactly.
```

**Validation:**
- [ ] All endpoints defined
- [ ] Proper async/await usage
- [ ] No blocking calls in request handlers
- [ ] WebSocket uses native LangGraph streaming

---

## Testing Phase

### Test 1: Service Startup

```bash
cd apps/agent-runtime
source .venv/bin/activate
uvicorn agent_runtime.main:app --reload
```

**Expected**: 
- Server starts on port 8000
- No import errors
- Health check returns 200 OK

**Evidence**: Screenshot or log output showing successful startup.

---

### Test 2: Database Connection

```bash
# Ensure Postgres is running
docker-compose up -d postgres

# Check tables created by checkpointer.setup()
docker exec -it <postgres-container> psql -U yfe -d yfe_db -c "\dt"
```

**Expected**:
- Tables `checkpoints`, `checkpoint_writes` exist (or similar per official LangGraph schema)

**Evidence**: SQL output showing tables.

---

### Test 3: End-to-End Task Execution

**Via cURL or Postman:**

```bash
# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a simple hello world function"}'

# Response: {"task_id": "abc-123", "status": "running"}

# Get status
curl http://localhost:8000/api/tasks/abc-123

# Expected: State showing plan and/or result
```

**Evidence**:
- Request/response logs
- Database state showing checkpointed data
- LLM was actually called (show API logs or response content)

---

### Test 4: Lint & Type Checks

```bash
ruff check src/
mypy src/ --ignore-missing-imports
```

**Expected**: Both pass with zero errors.

**Evidence**: Command output showing clean results.

---

## Documentation Phase

### D1: Session Log

Create: `docs/state/SESSIONS/2025-11-21_dev_fix001-implementation.md`

**Structure:**

```markdown
# Session Log: Restore Agent Runtime (TASK-FIX-001)

## Research Findings

### MCP Query 1: StateGraph Basics
- Query: "langgraph 1.0.3 StateGraph basic example"
- Key Finding: [paste relevant code example]
- Applied To: `graph.py` line X-Y
- Link: [official doc URL from MCP response]

[Repeat for all 6 queries]

## Implementation Decisions

### Decision 1: PostgresSaver Connection Pattern
- Question: How to initialize PostgresSaver in FastAPI context?
- Research: MCP Query 2 + Query 6
- Decision: [your choice]
- Rationale: [evidence from docs]
- Code: `graph.py:L45-L50`

### Decision 2: Streaming Pattern
- Question: How to stream events to WebSocket?
- Research: MCP Query 3, 4, 6
- Decision: [your choice]
- Rationale: [evidence from docs]
- Code: `routes.py:L78-L95`

[Document all major decisions]

## Test Results

### Test 1: Service Startup
- Command: `uvicorn ...`
- Result: ✅ PASS
- Evidence: [screenshot or log excerpt]

[All 4 tests documented with evidence]

## Code Changes

- Created: `api/__init__.py`, `api/routes.py`, `graph.py`
- Modified: None
- Lines Added: ~200
- All code verified against MCP query results

## Verification

- [ ] Service starts successfully
- [ ] Health check works
- [ ] End-to-end task completes
- [ ] Uses PostgresSaver (verified in DB)
- [ ] Uses native astream (verified in code)
- [ ] Lint clean
- [ ] Type safe
```

---

### D2: Update BLOCKERS.md

Add new blocker:

```markdown
## B-006: Agent Runtime Non-Functional (RESOLVED)

**Opened**: 2025-11-21  
**Severity**: CRITICAL  
**Status**: ✅ RESOLVED  

**Issue**: `apps/agent-runtime` missing `api/routes.py` and `graph.py`. Service could not start.

**Root Cause**: Files were never implemented or were lost in a git error.

**Resolution**: 
- Implemented `graph.py` with native LangGraph patterns per MCP queries
- Implemented `api/routes.py` with FastAPI endpoints
- Verified service startup and end-to-end execution
- Session log: `docs/state/SESSIONS/2025-11-21_dev_fix001-implementation.md`

**Resolved By**: Developer  
**Resolved On**: 2025-11-21  
```

---

### D3: Update PROGRESS.md

```markdown
## 2025-11-21 - Agent Runtime Restored (Phase 0 Continued)

**Completed**: Restored `apps/agent-runtime` to working state after audit revealed missing files.

**Changes**:
- Implemented `graph.py` with native LangGraph 1.0.3 patterns
- Implemented `api/routes.py` with FastAPI endpoints  
- Verified PostgresSaver checkpointing
- Verified native streaming with `astream`
- All patterns evidence-based from official LangChain docs via MCP

**Evidence**: 
- Service starts successfully
- End-to-end task execution works
- Session log: SESSIONS/2025-11-21_dev_fix001-implementation.md
- Tests: All lint, type, and runtime tests pass
```

---

## Success Criteria

You are DONE when:

- [ ] `apps/agent-runtime` service starts without errors
- [ ] Health check endpoint returns 200 OK
- [ ] Can create a task via POST /api/tasks
- [ ] Can retrieve task state via GET /api/tasks/{id}
- [ ] Task execution uses real LLM calls (not mocks)
- [ ] PostgresSaver is used (verified in database)
- [ ] Native `astream` is used (verified in code)
- [ ] All MCP queries documented in session log
- [ ] All implementation decisions cite MCP query evidence
- [ ] Lint clean (`ruff check` passes)
- [ ] Type safe (`mypy` passes)
- [ ] Session log complete with evidence
- [ ] BLOCKERS.md updated
- [ ] PROGRESS.md updated
- [ ] All code committed with detailed message

---

## Critical Reminders

1. **NO CUSTOM CODE IF NATIVE EXISTS**
   - Do NOT create custom streaming if `astream` exists
   - Do NOT create custom state if PostgresSaver exists
   - Every pattern must cite an MCP query result

2. **PRODUCTION FROM LINE 1**
   - No TODOs, no stubs, no "implement later"
   - Real LLM calls from character 1
   - Real database from character 1

3. **EVIDENCE REQUIRED**
   - Every design decision must cite official docs
   - Every test must have captured evidence
   - Session log must link MCP queries to code lines

4. **TYPE SAFETY & LINT**
   - Must pass `mypy` and `ruff` before submission
   - No `type: ignore` comments without justification

---

## CEO Review Checklist

When you submit, I will verify:

- [ ] Service actually runs (I will test `uvicorn` command)
- [ ] MCP queries were run and documented
- [ ] Code patterns match MCP query results (no custom deviations)
- [ ] Database tables exist (I will check Postgres)
- [ ] Real LLM was called (I will check logs/network)
- [ ] Session log has evidence (screenshots/logs, not just claims)
- [ ] No "TODO" or "stub" anywhere in new code

**If any item fails, task will be REJECTED and returned to you.**

---

## Timeline

**Start**: Immediately  
**Expected Duration**: 6-8 hours focused work  
**Deadline**: End of work session (notify CEO when complete)

---

## Questions?

If you encounter conflicting patterns in official docs, or if MCP queries return unexpected results:

1. Document the conflict in session log
2. State which pattern you chose and why
3. Cite specific doc URLs or query responses
4. Continue with evidence-based best judgment
5. Note it for CEO review

**Do NOT guess. Do NOT use generic patterns. ONLY use documented, evidence-based patterns.**
