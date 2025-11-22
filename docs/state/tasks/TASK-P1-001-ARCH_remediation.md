# TASK-P1-001-ARCH: Architecture Compliance Remediation

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL - BLOCKS P1-002**  
**Date**: 2025-11-22  
**Dependencies**: None  
**Blocks**: TASK-P1-002  
**Type**: Refactoring (NO LangGraph changes)

---

## Objective

Bring existing TASK-P1-001 implementation into compliance with the **5 Golden Architecture Rules** defined in `constitution/ARCHITECTURAL_DECISIONS.md` and validated by Research Brief RB-002.

**CRITICAL**: This task is **PURE REFACTORING**. The LangGraph implementation in `graph.py` is **already correct** and must NOT be changed. We are ONLY fixing the REST API wrapper, error handling, and file organization.

---

## What's Already Correct (DO NOT TOUCH)

✅ **LangGraph Implementation** (`graph.py`):
- StateGraph with proper AgentState
- Async nodes with real LLM calls
- Stream writer for custom events
- Checkpointer integration
- All MCP-validated patterns

✅ **Naming Convention**:
- Backend uses snake_case consistently
- Frontend uses snake_case for API models
- JSON responses use snake_case

**If your changes touch `planner_node()`, `executor_node()`, or graph construction logic → YOU ARE DOING IT WRONG.**

---

## Violations to Fix

### ❌ VIOLATION 1: API Versioning (Golden Rule #1)
**Current**: Unversioned endpoints
```python
# routes.py line 18
@router.post("/tasks", response_model=TaskResponse)

# routes.py line 43
@router.get("/tasks/{task_id}")

# routes.py line 56
@router.websocket("/tasks/{task_id}/stream")
```

**Required**: Add `/v1/` prefix
```python
@router.post("/v1/tasks", response_model=TaskResponse)
@router.get("/v1/tasks/{task_id}")
@router.websocket("/v1/tasks/{task_id}/stream")
```

**Frontend Changes**:
```typescript
// apps/web/src/lib/api.ts line 9
fetch(`${API_BASE_URL}/api/v1/tasks`, ...)

// apps/web/src/app/page.tsx line 24
const wsUrl = `ws://localhost:8002/api/v1/tasks/${taskId}/stream`;
```

---

### ❌ VIOLATION 2: Error Format (Golden Rule #2)
**Current**: Ad-hoc FastAPI HTTPException
```python
# routes.py line 51
raise HTTPException(status_code=404, detail="Task not found")

# routes.py line 54
raise HTTPException(status_code=500, detail=str(e))
```

**Required**: RFC 9457 Problem Details

**Step 1**: Create `apps/agent-runtime/src/agent_runtime/schemas/api/problem_detail.py`:
```python
from pydantic import BaseModel

class ProblemDetail(BaseModel):
    """RFC 9457 Problem Details for HTTP APIs."""
    type: str  # URI reference identifying the problem type
    title: str  # Short, human-readable summary
    status: int  # HTTP status code
    detail: str  # Explanation specific to this occurrence
    instance: str | None = None  # URI reference to specific occurrence
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "https://yfe.app/errors/task-not-found",
                "title": "Task Not Found",
                "status": 404,
                "detail": "Task a1b2c3d4 was not found in the system",
                "instance": "urn:trace:req-abc123"
            }
        }
```

**Step 2**: Create exception handler in `main.py`:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from .schemas.api.problem_detail import ProblemDetail

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Convert HTTPException to RFC 9457 Problem Details."""
    problem = ProblemDetail(
        type=f"https://yfe.app/errors/{exc.status_code}",
        title=exc.detail if isinstance(exc.detail, str) else "Error",
        status=exc.status_code,
        detail=str(exc.detail),
        instance=f"urn:trace:{request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump()
    )
```

---

### ❌ VIOLATION 3: File Structure (Golden Rule #4)
**Current**: Flat structure
```
agent_runtime/
├── api/
│   └── routes.py
├── graph.py
├── main.py
└── settings.py
```

**Required**: Organized packages
```
agent_runtime/
├── api/
│   └── routers/
│       └── tasks.py  # ← Rename routes.py → tasks.py, move here
├── graph/
│   ├── __init__.py
│   ├── graph.py  # ← Move from root
│   └── nodes/
│       ├── __init__.py
│       ├── planning.py  # ← Extract planner_node
│       └── execution.py  # ← Extract executor_node
├── schemas/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── problem_detail.py  # ← Created above
│   │   └── tasks.py  # ← Move TaskRequest, TaskResponse here
│   └── state.py  # ← Move AgentState here
├── main.py
└── settings.py
```

**Migration Steps**:

1. Create new directories:
   ```bash
   mkdir -p apps/agent-runtime/src/agent_runtime/graph/nodes
   mkdir -p apps/agent-runtime/src/agent_runtime/schemas/api
   mkdir -p apps/agent-runtime/src/agent_runtime/api/routers
   ```

2. Move `AgentState` to `schemas/state.py`:
   ```python
   # schemas/state.py
   from typing import TypedDict, Literal
   from langchain_core.messages import BaseMessage
   
   class AgentState(TypedDict):
       """State for the agent graph."""
       schema_version: Literal["1"]  # NEW: Version tracking
       task: str
       plan: str | None
       result: str | None
       messages: list[BaseMessage]
   ```

3. Move Pydantic models to `schemas/api/tasks.py`:
   ```python
   # schemas/api/tasks.py
   from pydantic import BaseModel
   
   class TaskRequest(BaseModel):
       task: str
   
   class TaskResponse(BaseModel):
       task_id: str
       status: str
   ```

4. Extract nodes to separate files:
   ```python
   # graph/nodes/planning.py
   from typing import Any
   from langchain_core.messages import HumanMessage
   from langgraph.config import get_stream_writer
   from ...schemas.state import AgentState
   from ..graph import get_llm  # If get_llm moves to graph.py
   
   async def planner_node(state: AgentState) -> dict[str, Any]:
       """Create a plan from task description."""
       # [COPY EXACT CODE FROM CURRENT graph.py lines 37-56]
       # DO NOT MODIFY LOGIC
   ```

   ```python
   # graph/nodes/execution.py
   from typing import Any
   from langchain_core.messages import HumanMessage
   from langgraph.config import get_stream_writer
   from ...schemas.state import AgentState
   from ..graph import get_llm
   
   async def executor_node(state: AgentState) -> dict[str, Any]:
       """Execute the plan."""
       # [COPY EXACT CODE FROM CURRENT graph.py lines 58-77]
       # DO NOT MODIFY LOGIC
   ```

5. Update `graph/graph.py`:
   ```python
   # graph/graph.py
   from typing import Any
   from langchain_anthropic import ChatAnthropic
   from langchain_openai import ChatOpenAI
   from langgraph.graph import END, START, StateGraph
   from pydantic import SecretStr
   
   from ..settings import settings
   from ..schemas.state import AgentState
   from .nodes.planning import planner_node
   from .nodes.execution import executor_node
   
   def get_llm() -> ChatAnthropic | ChatOpenAI:
       """Get configured LLM based on settings."""
       # [COPY EXACT CODE FROM CURRENT graph.py lines 23-35]
   
   def create_graph(checkpointer: Any) -> Any:
       """Create and return compiled LangGraph."""
       # [COPY EXACT CODE FROM CURRENT graph.py lines 81-92]
       # Update imports but DO NOT change logic
   ```

6. Rename and move `api/routes.py` → `api/routers/tasks.py`:
   ```python
   # api/routers/tasks.py
   from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, WebSocket
   from ...schemas.api.tasks import TaskRequest, TaskResponse
   from ...graph.graph import create_graph  # Updated import
   
   router = APIRouter()
   
   @router.post("/v1/tasks", response_model=TaskResponse)  # ← Added /v1/
   async def create_task(...):
       # [SAME LOGIC, just updated route]
   
   @router.get("/v1/tasks/{task_id}")  # ← Added /v1/
   async def get_task_status(...):
       # [SAME LOGIC, just updated route]
   
   @router.websocket("/v1/tasks/{task_id}/stream")  # ← Added /v1/
   async def stream_task(...):
       # [SAME LOGIC, just updated route]
   ```

7. Update `main.py` imports:
   ```python
   # main.py
   from .api.routers.tasks import router as tasks_router  # Updated import
   from .graph.graph import create_graph  # Updated import
   
   # Router inclusion (line 57)
   app.include_router(tasks_router, prefix="/api")  # Prefix stays /api, routes have /v1/
   ```

---

### ⚠️ VIOLATION 4: State Schema Version (Golden Rule #3)
**Current**: No version tracking
```python
class AgentState(TypedDict):
    task: str
    plan: str | None
    result: str | None
    messages: list[BaseMessage]
```

**Required**: Add `schema_version` field
```python
from typing import Literal

class AgentState(TypedDict):
    schema_version: Literal["1"]  # NEW: Track schema version
    task: str
    plan: str | None
    result: str | None
    messages: list[BaseMessage]
```

**Update graph initialization** to set version:
```python
# graph/graph.py - create_graph or node that initializes state
inputs = {
    "schema_version": "1",  # NEW
    "task": task_request.task,
    "messages": []
}
```

---

## Implementation Checklist

### Phase A: Error Format (30 min)
- [ ] Create `schemas/api/__init__.py`
- [ ] Create `schemas/api/problem_detail.py`
- [ ] Add exception handler to `main.py`
- [ ] Test: `curl http://localhost:8002/api/tasks/nonexistent` returns RFC 9457 format

### Phase B: File Reorganization (60 min)
- [ ] Create directory structure (`graph/`, `graph/nodes/`, `schemas/`, `api/routers/`)
- [ ] Create all `__init__.py` files
- [ ] Move `AgentState` → `schemas/state.py` (add `schema_version`)
- [ ] Move `TaskRequest`, `TaskResponse` → `schemas/api/tasks.py`
- [ ] Extract `planner_node` → `graph/nodes/planning.py` (NO LOGIC CHANGES)
- [ ] Extract `executor_node` → `graph/nodes/execution.py` (NO LOGIC CHANGES)
- [ ] Extract `get_llm` → `graph/graph.py`
- [ ] Update `create_graph` in `graph/graph.py` with new imports
- [ ] Rename `api/routes.py` → `api/routers/tasks.py`
- [ ] Update all imports in `main.py`
- [ ] Delete old files (`graph.py` at root, `api/routes.py`)

### Phase C: API Versioning (15 min)
- [ ] Update `api/routers/tasks.py`: Add `/v1/` to all 3 routes
- [ ] Update `apps/web/src/lib/api.ts`: Change `/api/tasks` → `/api/v1/tasks`
- [ ] Update `apps/web/src/app/page.tsx`: Change WebSocket URL to `/api/v1/tasks/${taskId}/stream`

### Phase D: Verification (30 min)
- [ ] Lint: `ruff check apps/agent-runtime/src`
- [ ] Type check: `mypy apps/agent-runtime/src`
- [ ] Docker build: `docker-compose build`
- [ ] Docker run: `docker-compose up -d`
- [ ] Test POST: `curl -X POST http://localhost:8002/api/v1/tasks -H "Content-Type: application/json" -d '{"task":"test"}'`
- [ ] Test GET: `curl http://localhost:8002/api/v1/tasks/{id}`
- [ ] Test error: `curl http://localhost:8002/api/v1/tasks/fake` → Returns RFC 9457
- [ ] Test frontend: `open http://localhost:3000` → Task submission works
- [ ] Verify logs: `docker logs yfe-agent-runtime` → No errors

---

## Quality Gates

### G1: Research (N/A for refactoring)
- No new patterns introduced

### G3: Lint Clean
- [ ] `ruff check` passes
- [ ] No new lint errors

### G5: Type Safe
- [ ] `mypy` passes
- [ ] All imports resolve correctly

### G6: Builds in Docker
- [ ] `docker-compose build` succeeds
- [ ] All 3 containers start healthy

### G10: Owner Can Use
- [ ] Owner Console still works
- [ ] Task submission succeeds
- [ ] Events stream correctly
- [ ] No user-facing breakage

---

## Evidence Required

1. **File structure screenshot**:
   ```bash
   tree apps/agent-runtime/src/agent_runtime/ -I __pycache__
   ```

2. **API versioning proof**:
   ```bash
   curl -X POST http://localhost:8002/api/v1/tasks \
     -H "Content-Type: application/json" \
     -d '{"task":"Hello"}' | jq
   ```

3. **Error format proof**:
   ```bash
   curl http://localhost:8002/api/v1/tasks/nonexistent | jq
   # Should return RFC 9457 with "type", "title", "status", "detail"
   ```

4. **Docker logs** showing healthy startup

5. **Frontend screenshot** showing task submission still works

---

## Critical Rules

### 1. DO NOT Change LangGraph Logic
- `planner_node` logic: COPY, DON'T EDIT
- `executor_node` logic: COPY, DON'T EDIT
- Graph construction: COPY, DON'T EDIT
- **Only change**: File location and imports

### 2. Backward Compatibility
- Old checkpoints with no `schema_version` must still work
- Handle missing `schema_version` gracefully in nodes:
  ```python
  version = state.get("schema_version", "1")  # Default to "1" if missing
  ```

### 3. Import Paths
- Use absolute imports: `from agent_runtime.graph.graph import create_graph`
- Update ALL import statements consistently

### 4. Docker from Line 1
- Test ONLY in Docker
- Provide all 5 evidence screenshots from Docker
- No local testing allowed

---

## Timeline

**Total**: 2-3 hours  
**Breakdown**:
- Error format: 30 min
- File reorganization: 60 min
- API versioning: 15 min
- Verification: 30-45 min

---

## Session Log

Create: `docs/state/SESSIONS/2025-11-22_dev_p1001-arch-remediation.md`

**Must include**:
- File migration steps with git mv commands
- Import path updates
- Before/after directory tree
- All 5 evidence items
- Confirmation: "LangGraph logic unchanged, only file organization"

---

## Success Criteria

**APPROVED if**:
1. ✅ All routes use `/v1/` prefix
2. ✅ All errors return RFC 9457 format
3. ✅ Files organized per ARCHITECTURAL_DECISIONS.md
4. ✅ `AgentState` has `schema_version` field
5. ✅ All tests pass (existing functionality intact)
6. ✅ Docker build + run succeeds
7. ✅ Owner Console still works end-to-end

**REJECTED if**:
- LangGraph node logic changed
- Existing functionality broken
- Missing evidence
- Imports broken

---

**This is pure refactoring. Move files, update imports, add version field. That's it.**
