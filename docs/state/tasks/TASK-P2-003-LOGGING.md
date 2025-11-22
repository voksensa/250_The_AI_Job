# TASK-P2-003-LOGGING: Add Structured Logging

**Priority**: MEDIUM  
**Order**: Task 3 of 4 (Phase 2 Foundation)  
**Depends On**: TASK-P2-002-OPENAPI  
**Estimated**: 2 hours

---

## Objective

Replace scattered `print()` statements with structured logging for production observability.

**Golden Rule**: Rule 4.11 from RB-003 (Tier 2)

---

## Current State

**Backend Logging**:
- Uses `print()` for debug (e.g., "DEBUG: Running lint_gate_node")
- No structured logging
- No log levels
- No context (request IDs, user IDs, etc.)

**Frontend**: Browser console only

---

## Tasks

### Phase A: Setup Structured Logging (45min)

**Install**: Python `structlog`

**Create**: `apps/agent-runtime/src/agent_runtime/utils/logger.py`

```python
import structlog

def get_logger(name: str):
    return structlog.get_logger(name)

# Configure processors
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
```

---

### Phase B: Replace print() Statements (45min)

**Files to Update**:
- `graph/nodes/gates.py` (9 print statements)
- `graph/nodes/planning.py` 
- `graph/nodes/execution.py`
- `api/routers/tasks.py`

**Pattern**:
```python
# OLD
print("DEBUG: Running lint_gate_node")

# NEW
logger = get_logger(__name__)
logger.info("gate_execution", gate="lint", status="starting")
```

**Add Context**:
- `task_id` 
- `node_name`
- `status`
- Execution time

---

### Phase C: Log Errors with Context (30min)

**Error Logging**:
```python
try:
    result = await execute()
except Exception as e:
    logger.error(
        "task_execution_failed",
        task_id=task_id,
        error=str(e),
        exc_info=True
    )
    raise
```

---

## Success Criteria

✅ **No print() in production code**: All replaced  
✅ **Structured**: JSON log format  
✅ **Contextual**: task_id, node_name in all logs  
✅ **Levels**: info, warning, error used correctly  
✅ **Errors**: Full stack traces captured

---

## Next Task

After completion → **TASK-P2-004-METRICS**
