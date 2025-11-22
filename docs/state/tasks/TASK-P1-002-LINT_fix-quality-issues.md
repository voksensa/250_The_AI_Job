# TASK-P1-002-LINT: Fix Lint and Type Errors

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL - BLOCKS P1-002 APPROVAL**  
**Date**: 2025-11-22  
**Type**: Quality Remediation

---

## Objective

Fix all lint warnings and type errors in TASK-P1-002 before Owner grants final approval.

**Current Issues**:
- 39 lint warnings (formatting, import sorting)
- 1 type error (`execution.py:11`)

**Success**: Clean `ruff check` and `mypy` output.

---

## Phase A: Auto-Fix Lint Warnings (5 min)

**Command**:
```bash
cd apps/agent-runtime
ruff check --fix src/agent_runtime/
```

**Expected**: Fixes 30/39 warnings automatically (W293, I001)

**Verify**:
```bash
ruff check src/agent_runtime/
# Should show ~9 remaining warnings
```

---

## Phase B: Fix Type Error (10 min)

**File**: `apps/agent-runtime/src/agent_runtime/graph/nodes/execution.py`

**Current Code** (line 11):
```python
async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    llm = get_llm()
    
    plan = state["plan"]  # ← ERROR: "str | None" is not indexable
    # ...
```

**Fix**:
```python
async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    llm = get_llm()
    
    # Check if plan exists
    plan = state.get("plan")
    if not plan:
        return {"result": "Error: No plan was generated"}
    
    # Now TypeScript knows plan is str, not None
    prompt = HumanMessage(
        content=f"Execute this plan:\n\n{plan}\n\nProvide implementation details."
    )
    # ... rest of function unchanged
```

**Verify**:
```bash
mypy src/agent_runtime --ignore-missing-imports
# Should show: Success: no issues found
```

---

## Phase C: Manual Lint Fixes (15 min)

**Remaining warnings** (likely 9 issues after auto-fix):

Check output of `ruff check src/` and fix any remaining:
- Remove trailing whitespace
- Fix any missed import sorting
- Ensure all blank lines are clean

**Verify**:
```bash
ruff check src/agent_runtime/
# Should show: All checks passed!
```

---

## Phase D: Docker Verification (10 min)

**Rebuild**:
```bash
docker compose down
docker compose build
docker compose up -d
```

**Verify**:
- All containers healthy
- No new errors in logs
- Feature still works (submit task, gates pass, toggle appears)

---

## Evidence Required

1. **Lint output**:
   ```bash
   ruff check src/agent_runtime/ > evidence/lint_clean.txt
   ```

2. **Type check output**:
   ```bash
   mypy src/agent_runtime --ignore-missing-imports > evidence/type_check.txt
   ```

3. **Docker proof**:
   ```bash
   docker ps --filter "name=yfe" > evidence/containers_healthy.txt
   ```

4. **Session log**: `docs/state/SESSIONS/2025-11-22_dev_p1002-lint-fixes.md`

---

## Success Criteria

✅ **APPROVED if**:
1. `ruff check src/agent_runtime/` → 0 warnings, 0 errors
2. `mypy src/agent_runtime --ignore-missing-imports` → Success
3. Docker builds and runs
4. Feature still functional (no regressions)
5. Session log created
6. Git commit with all fixes

❌ **REJECTED if**:
- Any lint warnings remain
- Type errors remain
- Docker build fails
- Feature broken

---

## Timeline

**Total**: 40 minutes  
- Auto-fix: 5 min
- Type fix: 10 min
- Manual fixes: 15 min
- Docker verify: 10 min

---

## After Completion

**Developer** submits for CEO review with:
- Evidence files (lint, type, Docker)
- Session log
- Confirmation: "All lint/type issues fixed"

**CEO** verifies and requests Owner final approval.

**Owner** grants final approval → P1-002 COMPLETE → Proceed to Phase 2.
