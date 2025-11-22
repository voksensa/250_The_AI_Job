# TASK-P1-002: Production Toggle Switch Implementation

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL - Killer Feature #1**  
**Date**: 2025-11-22  
**Phase**: Phase 1 - Production Toggle MVP  
**Depends On**: TASK-P1-001 (Complete)  
**Blocks**: All future Phase 1 tasks

---

## Objective

Implement the **Production Toggle Switch** - the first killer feature from VISION.md. Owner must see a visual toggle that:
- Is **DISABLED** until quality gates pass (lint, tests)
- Turns **GREEN** when gates pass
- When clicked, deploys app to "production" environment

**This is not just a UI switch - it's the core gating mechanism for production quality.**

---

## Success Criteria

**From Owner Console (browser, Docker):**

1. Submit a task → See "Production Mode" toggle **grayed out/disabled**
2. Watch as system runs quality gates (lint, tests)
3. See toggle turn **green** when all gates pass
4. Click toggle → App deploys to production environment
5. See "Production: ENABLED" indicator with deployment URL

**All verified in Docker, screenshots required.**

---

## Mandatory Research (MCP Queries)

Before writing ANY code, run these MCP queries and document in session log:

### R1: LangGraph Conditional Edges for Quality Gates
**Query**: "LangGraph 1.0.3 conditional edges based on state properties"  
**Why**: Need to route graph flow based on gate results (pass/fail)

### R2: LangGraph State Updates from Nodes
**Query**: "LangGraph 1.0.3 how to update state from node execution"  
**Why**: Quality gate nodes must update state with pass/fail status

### R3: LangGraph Checkpointer for Interrupts
**Query**: "LangGraph 1.0.3 human-in-the-loop interrupts with checkpointer"  
**Why**: Production toggle is a human decision point, need to pause execution

### R4: React State Management for Toggle
**Query**: "React useState for toggle button with disabled state"  
**Why**: Frontend toggle must reflect backend gate status

### R5: WebSocket State Updates
**Query**: "WebSocket send state updates from server to client in real-time"  
**Why**: Gate status changes must stream to UI immediately

**Document all findings in**: `docs/state/SESSIONS/2025-11-22_dev_p1002-research.md`

---

## Architecture (Native LangGraph Only)

### Backend: Quality Gate Nodes

**Add to `graph.py` (extend existing graph)**:

```python
# New nodes (MUST cite MCP R1, R2 in comments)
def lint_gate_node(state: AgentState) -> dict:
    """Run ruff check on generated code."""
    # MCP R2: State update pattern
    # Run: ruff check <code>
    # Return: {"lint_status": "pass" | "fail", "lint_errors": [...]}

def test_gate_node(state: AgentState) -> dict:
    """Run pytest on generated code."""
    # MCP R2: State update pattern  
    # Run: pytest <code>
    # Return: {"test_status": "pass" | "fail", "test_results": {...}}

def production_gate_check(state: AgentState) -> str:
    """Conditional edge: check if all gates passed."""
    # MCP R1: Conditional routing pattern
    if state["lint_status"] == "pass" and state["test_status"] == "pass":
        return "ready_for_production"
    return "not_ready"

def production_interrupt_node(state: AgentState) -> dict:
    """Human-in-the-loop: wait for production toggle."""
    # MCP R3: Interrupt pattern
    # This node PAUSES execution until Owner clicks toggle
    return {"production_approved": None}  # Waits for human input

# Wire into graph (cite MCP R1)
workflow.add_node("lint_gate", lint_gate_node)
workflow.add_node("test_gate", test_gate_node)
workflow.add_node("production_decision", production_interrupt_node)

# Conditional edges (cite MCP R1)
workflow.add_conditional_edges(
    "executor",
    production_gate_check,
    {
        "ready_for_production": "production_decision",
        "not_ready": "executor"  # Loop back to fix
    }
)
```

**Key Requirements:**
- Use `add_conditional_edges` (native LangGraph pattern)
- Use `interrupt` for human decision
- Update `AgentState` TypedDict with new fields
- NO custom gate runners - use native node execution

---

### Frontend: Production Toggle UI

**Add to `apps/web/src/app/page.tsx`**:

```tsx
// MCP R4: Toggle state pattern
const [productionReady, setProductionReady] = useState(false);
const [productionEnabled, setProductionEnabled] = useState(false);

// MCP R5: WebSocket listener for gate updates
useEffect(() => {
  if (!wsRef.current) return;
  
  wsRef.current.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Listen for gate status updates
    if (data.lint_status && data.test_status) {
      const ready = data.lint_status === 'pass' && data.test_status === 'pass';
      setProductionReady(ready);
    }
    
    // Listen for production approval
    if (data.production_approved !== undefined) {
      setProductionEnabled(data.production_approved);
    }
  };
}, [taskId]);

// Production Toggle Component
<div className="border-t pt-4">
  <h3 className="font-semibold mb-2">Production Mode</h3>
  <button
    disabled={!productionReady}
    onClick={() => handleToggle()}
    className={productionReady ? 'bg-green-600' : 'bg-gray-400'}
  >
    {productionReady ? '✓ Deploy to Production' : '⊗ Quality Gates Required'}
  </button>
  
  <div className="mt-2 text-sm">
    <div>Lint: {lintStatus === 'pass' ? '✓' : '×'}</div>
    <div>Tests: {testStatus === 'pass' ? '✓' : '×'}</div>
  </div>
</div>
```

**Key Requirements:**
- Toggle MUST be disabled until gates pass
- Visual indicators for each gate (✓/×)
- Click sends approval to backend via WebSocket
- Tailwind CSS styling (green when ready, gray when not)

---

## Implementation Plan

### Phase A: Backend Quality Gates

1. **Update `AgentState`** (cite MCP R2):
   ```python
   class AgentState(TypedDict):
       messages: List[BaseMessage]
       task: str
       plan: str
       result: str
       lint_status: str  # NEW
       test_status: str  # NEW
       production_approved: bool | None  # NEW
   ```

2. **Add gate nodes** to `graph.py`:
   - `lint_gate_node`: Run ruff check
   - `test_gate_node`: Run pytest
   - Both update state, emit custom events

3. **Add conditional routing** (cite MCP R1):
   - `production_gate_check` function
   - Routes to production_decision if ready, else loops back

4. **Add interrupt node** (cite MCP R3):
   - `production_interrupt_node` pauses execution
   - Waits for WebSocket message with approval

5. **Update routes.py**:
   - Handle WebSocket message with `production_approved: true`
   - Resume graph execution with approval

---

### Phase B: Frontend Toggle UI

1. **Update `page.tsx`**:
   - Add productionReady state
   - Add WebSocket listener for gate updates
   - Add toggle button component
   - Add gate status indicators

2. **Styling**:
   - Disabled: Gray, cursor not-allowed
   - Ready: Green, pulsing animation
   - Enabled: Blue, shows deployment URL

3. **WebSocket flow**:
   - Backend sends: `{lint_status: 'pass', test_status: 'pass'}`
   - Frontend enables toggle
   - User clicks → sends: `{production_approved: true}`
   - Backend resumes → deploys → sends: `{production_deployed: true, url: '...'}`

---

## Docker Verification Requirements

**You MUST provide these screenshots from Docker:**

1. **docker-compose build** output showing success
2. **docker ps** showing all 3 containers healthy
3. **Browser: Toggle disabled** (gates not run yet)
4. **Browser: Gates running** (lint/test in progress)
5. **Browser: Toggle enabled** (gates passed)
6. **Browser: Production deployed** (after toggle click)
7. **docker logs yfe-agent-runtime** showing gate execution

**Session log MUST include**:
- All 5 MCP query results with citations
- Code snippets citing which MCP pattern used
- Screenshot evidence embedded

---

## Quality Gates (This Task)

### G1: Research Complete
- [ ] All 5 MCP queries run and documented
- [ ] Session log has query results
- [ ] Code cites MCP patterns in comments

### G3: Lint Clean
- [ ] `ruff check` passes (backend)
- [ ] `eslint` passes (frontend)

### G5: Type Safe
- [ ] `mypy` passes (backend)
- [ ] `tsc --noEmit` passes (frontend)

### G6: Builds in Docker
- [ ] `docker-compose build` succeeds
- [ ] No build errors

### G10: Owner Can Use
- [ ] Owner can see toggle in browser
- [ ] Toggle works (disabled → enabled → deploy)
- [ ] Validated in ≤20 min

---

## Success Checklist (For Developer)

**Research Phase:**
- [ ] Run MCP R1: LangGraph conditional edges
- [ ] Run MCP R2: LangGraph state updates
- [ ] Run MCP R3: LangGraph interrupts
- [ ] Run MCP R4: React toggle state
- [ ] Run MCP R5: WebSocket real-time updates
- [ ] Document all in session log with code examples

**Implementation Phase:**
- [ ] Update `AgentState` TypedDict with new fields
- [ ] Add `lint_gate_node` with ruff check
- [ ] Add `test_gate_node` with pytest
- [ ] Add `production_gate_check` conditional function
- [ ] Add `production_interrupt_node` for human approval
- [ ] Wire nodes with `add_conditional_edges`
- [ ] Update `routes.py` to handle toggle approval
- [ ] Add toggle UI component to `page.tsx`
- [ ] Add WebSocket listener for gate status
- [ ] Add gate indicators (✓/×) to UI
- [ ] Test in Docker (all 7 screenshots)

**Verification Phase:**
- [ ] Build containers: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Verify all healthy: `docker ps`
- [ ] Open browser: http://localhost:3000
- [ ] Submit task → Capture screenshot (toggle disabled)
- [ ] Watch gates run → Capture screenshot (gates running)
- [ ] Toggle enabled → Capture screenshot (gates passed)
- [ ] Click toggle → Capture screenshot (production deployed)
- [ ] Check logs: `docker logs yfe-agent-runtime`
- [ ] Lint/type checks pass
- [ ] Session log complete with evidence

**Documentation Phase:**
- [ ] Session log: `docs/state/SESSIONS/2025-11-22_dev_p1002-implementation.md`
- [ ] Screenshots in: `evidence/G10/p1002-toggle/`
- [ ] Update `PROGRESS.md`
- [ ] Git commit with detailed message

---

## CEO Review Protocol

**I will verify by running:**

```bash
# Clean slate
docker-compose down
docker system prune -f

# Build
docker-compose build

# Start
docker-compose up -d

# Wait
sleep 30

# Test
open http://localhost:3000
# 1. Submit task
# 2. Watch toggle (should be disabled)
# 3. Wait for gates
# 4. Toggle should turn green
# 5. Click toggle
# 6. Verify production deployment

# Check logs
docker logs yfe-agent-runtime | grep -i "lint\|test\|production"
```

**If ANY step fails → REJECTED**

---

## Critical Reminders

### 1. Native LangGraph Only
- Use `add_conditional_edges` (not custom routers)
- Use `interrupt` (not custom pause mechanisms)
- Use `astream` with custom events (not manual broadcasting)
- Cite MCP patterns in every function

### 2. Docker from Line 1
- Test ONLY in Docker (never local uvicorn/npm)
- Provide 7 screenshots from Docker execution
- No Docker proof = Automatic rejection

### 3. Evidence Required
- MCP queries documented with results
- Code must cite which MCP pattern used
- Screenshots showing toggle working
- Session log with full trail

### 4. This is Killer Feature #1
- **VISION.md** says: "Simple switch for prototype vs production"
- This makes or breaks the product
- Owner MUST feel confident clicking that toggle
- If toggle is confusing or unreliable → Mission failed

---

## Timeline

**Start**: Immediately  
**Expected Duration**: 6-8 hours focused work  
**Deadline**: End of work session

**Research**: 2 hours (5 MCP queries + documentation)  
**Backend**: 3 hours (4 new nodes + wiring)  
**Frontend**: 2 hours (Toggle UI + WebSocket)  
**Verification**: 1 hour (Docker testing + screenshots)

---

## Questions?

**If LangGraph patterns unclear:**
- Run MCP query first
- Document exact pattern from official docs
- Ask CEO if conflicting information

**If Docker build fails:**
- Share full build output in session log
- Check Dockerfile syntax
- Verify all dependencies in pyproject.toml

**If toggle behavior unclear:**
- It should be EXACTLY like a light switch
- Gray/disabled = can't flip
- Green = can flip
- Blue = already flipped

**NO GUESSING. Evidence-based only. LangGraph native only. Docker proof required.**

---

**Go build the first killer feature. Make it work like magic.**
