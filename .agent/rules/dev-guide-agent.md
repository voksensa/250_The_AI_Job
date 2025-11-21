---
trigger: model_decision
description: always follow if you are invoked as a developer
---

# Developer Guide: Building "Your First Engineer"

**Version**: 3.0 (Updated with Execution Framework)  
**Date**: 2025-11-21  
**Audience**: Developers implementing the system

---

## Start Here

**Read VISION.md first.** We're building:
> The first product that turns plain-language ideas into production-ready apps.

The 3 killer features:
1. Production Toggle
2. AI Test Users  
3. Build Story

**Everything you build must serve this vision.**

---

## Core Principles

### 1. Production from Line 1
- No stubs, no mocks, no "TODO: implement later"
- Real LLM calls, real Docker, real databases
- If it ships, it works

### 2. Non-Technical Owner First
- Owner must validate every feature in ≤20 min via browser
- No JSON editing, no terminal, no code reading required
- Simple English, visual feedback

### 3. Phase A + Phase B Together
- Backend capability + Frontend UI in same task
- Owner must SEE and USE every feature
- No backend-only deliverables

### 4. Evidence-Based Quality Gates
- See `constitution/NOVEMBER_2025_STANDARDS.md` for all thresholds
- Every task produces evidence in `evidence/G{N}/`
- CEO approves based on evidence, not trust

---

## Execution Framework

**Before starting any task, read:**
1. `constitution/EXECUTION_PROTOCOL_SPEC.md` - Full developer protocol
2. `constitution/NOVEMBER_2025_STANDARDS.md` - Tool versions & thresholds
3. `evidence/.template/README.md` - Evidence structure

**For each task:**
1. **Pre-Work:** `EXECUTION_PROTOCOL_SPEC.md` §2.2
2. **Implementation:** `EXECUTION_PROTOCOL_SPEC.md` §2.3
3. **Evidence Collection:** `EXECUTION_PROTOCOL_SPEC.md` §2.4
4. **Handoff to CEO:** `EXECUTION_PROTOCOL_SPEC.md` §2.5

---

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Orchestration**: LangGraph 1.0.3 (parallel, conditional, self-healing)
- **LLMs**: GPT-4, Claude 4.5, o-series
- **Database**: PostgreSQL + pgvector
- **Persistence**: PostgresSaver (not MemorySaver)
- **Execution**: Docker containers

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: React hooks (no Redux)

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Testing**: Pytest 9.0.x (backend), Vitest 4.x (frontend)
- **Linting**: Ruff (Python), ESLint 9.39.x (TypeScript)
- **Type Checking**: mypy 1.18.x (Python), tsc (TypeScript)

**See `constitution/NOVEMBER_2025_STANDARDS.md` §2 for pinned versions.**

---

## Architecture Patterns

### LangGraph Workflow

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("frontend_dev", frontend_node)
workflow.add_node("backend_dev", backend_node)
workflow.add_node("tester", test_node)

# Parallel execution
workflow.add_edge("planner", "frontend_dev")
workflow.add_edge("planner", "backend_dev")

# Fan-in to testing
workflow.add_edge("frontend_dev", "tester")
workflow.add_edge("backend_dev", "tester")

# End
workflow.add_edge("tester", END)

graph = workflow.compile(checkpointer=PostgresSaver(...))
```

### State Management

```python
from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[BaseMessage]
    task: str
    plan: Dict[str, str]
    code_files: Dict[str, str]
    test_results: Dict[str, Any]
    errors: List[str]
    status: str
```

### Self-Healing Loop

```python
from langgraph.types import task, RetryPolicy

@task(retry_policy=RetryPolicy(
    max_attempts=3,
    backoff_factor=2.0
))
async def fix_code(state: AgentState):
    errors = state["errors"]
    # Analyze and fix
    fixed_code = await analyze_and_fix(errors)
    return {"code_files": fixed_code}
```

---

## Building The 3 Killer Features

### Feature 1: Production Toggle

**Goal**: Simple switch that triggers full FAANG pipeline.

**Implementation**:
```python
# In workflow
def should_run_production_checks(state: AgentState) -> str:
    if state.get("production_mode"):
        return "full_pipeline"
    return "quick_prototype"

workflow.add_conditional_edges(
    "code_complete",
    should_run_production_checks,
    {
        "full_pipeline": "security_scan",
        "quick_prototype": "deploy"
    }
)
```

**Quality Checks (Production Mode)**:
- Testing: ≥80% coverage (backend), ≥70% (frontend)
- Security: SAST clean (0 critical/high)
- AI Risk: NIST AI RMF assessment
- Accessibility: WCAG 2.2 AA

**See `constitution/NOVEMBER_2025_STANDARDS.md` G5, G3, G9, G10 for thresholds.**

### Feature 2: AI Test Users

**Goal**: Synthetic users test app before real people.

**Implementation**:
```python
async def synthetic_qa_node(state: AgentState):
    # Define personas
    personas = [
        {"role": "guest", "scenario": "book_stay"},
        {"role": "host", "scenario": "create_listing"},
        {"role": "fraudster", "scenario": "test_payment_edge_cases"}
    ]
    
    results = []
    for persona in personas:
        result = await run_synthetic_user(
            persona=persona,
            app_url=state["preview_url"]
        )
        results.append(result)
    
    return {"test_results": results}
```

**Key Components**:
- Browser automation (Playwright)
- LLM-driven user behavior
- Flow library (sign up, checkout, cancel)
- Human-readable reports

**Evidence**: `evidence/G6/TASK-{ID}-synthetic-report.md`

### Feature 3: Build Story

**Goal**: Timeline showing what AI did in plain English.

**Implementation**:
```python
# Event tracking
class TimelineEvent(BaseModel):
    timestamp: datetime
    node: str
    action: str
    summary: str  # LLM-generated plain English
    details: Dict[str, Any]

# In each node
async def planner_node(state: AgentState):
    # Do work
    plan = create_plan(state["task"])
    
    # Log event
    timeline_event = TimelineEvent(
        timestamp=now(),
        node="planner",
        action="create_plan",
        summary=f"Chose {plan['tech_stack']} for marketplace app",
        details=plan
    )
    
    return {
        "plan": plan,
        "timeline": state.get("timeline", []) + [timeline_event]
    }
```

**UI Component**:
- Visual timeline
- Expandable details per step
- Code diffs, test logs
- Export as PDF

---

## Code Standards

### Python
```python
# Good
async def generate_code(state: AgentState) -> Dict[str, Any]:
    """Generate code files based on plan.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with code_files
    """
    code = await llm.ainvoke(...)
    return {"code_files": code}

# Bad
def gen(s):  # No types, no docstring
    return llm(s)
```

**Quality Gates:**
- Lint: Ruff clean (0 errors, 0 warnings)
- Types: mypy strict (0 errors)
- Evidence: `evidence/G4/TASK-{ID}-lint.txt`

### TypeScript
```typescript
// Good
interface BuildState {
  status: 'building' | 'testing' | 'ready';
  progress: number;
}

async function startBuild(task: string): Promise<BuildState> {
  const response = await fetch('/api/build', {
    method: 'POST',
    body: JSON.stringify({ task })
  });
  return response.json();
}

// Bad
function build(t) {  // No types
  return fetch('/api/build', { body: t });
}
```

**Quality Gates:**
- Lint: ESLint 9.39.x (0 errors, 0 warnings)
- Types: tsc strict (0 errors)
- Evidence: `evidence/G4/TASK-{ID}-lint.txt`

---

## Testing Requirements

### Backend Tests
```python
# test_workflow.py
async def test_production_toggle():
    """Test that production mode enforces quality gates."""
    engine = AgentEngine()
    
    # Prototype mode
    result = await engine.run_task(
        "Build simple app",
        production_mode=False
    )
    assert result["status"] == "complete"
    assert "test_results" not in result  # No tests in prototype
    
    # Production mode
    result = await engine.run_task(
        "Build simple app",
        production_mode=True
    )
    assert result["status"] == "complete"
    assert result["test_results"]["coverage"] >= 80
    assert result["security_scan"]["passed"] == True
```

**Coverage:** ≥80% line coverage for new backend code.

### Frontend Tests
```typescript
// BuildPage.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('production toggle shows quality checks', async () => {
  render(<BuildPage />);
  
  // Toggle production mode
  const toggle = screen.getByRole('switch', { name: /production/i });
  await userEvent.click(toggle);
  
  // Verify UI shows production checks
  await waitFor(() => {
    expect(screen.getByText(/Running security scan/i)).toBeInTheDocument();
  });
});
```

**Coverage:** ≥70% line coverage for new frontend code.

**Evidence:** `evidence/G5/TASK-{ID}-coverage-summary.txt`

---

## Task Workflow

**For every task, follow `constitution/EXECUTION_PROTOCOL_SPEC.md` §2:**

### 1. Pre-Work Checklist (§2.2)
- [ ] Read `TASK-{ID}.md` top-to-bottom
- [ ] Open `ROADMAP_SPEC.md` and verify phase alignment
- [ ] Open `NOVEMBER_2025_STANDARDS.md` for tool versions
- [ ] Create working branch: `feature/TASK-{ID}-{slug}`
- [ ] Update `docs/state/task.md` with current task

### 2. Implementation (§2.3)
- [ ] Design: Sketch solution in TASK file
- [ ] Code: Implement in smallest slices
- [ ] Tests: Add/extend unit + integration tests
- [ ] Static Analysis: Run lint + type checks
- [ ] Coverage: Generate reports for evidence

### 3. Evidence Collection (§2.4)
**For each gate in scope, create:**
- G1 (Research): `evidence/G1/TASK-{ID}-research-report.md`
- G2 (Architecture): `evidence/G2/TASK-{ID}-design.md`
- G3 (Security): `evidence/G3/TASK-{ID}-threat-model.md`
- G4 (Code Quality): `evidence/G4/TASK-{ID}-lint.txt`
- G5 (Testing): `evidence/G5/TASK-{ID}-coverage-summary.txt`
- G6-G11: See `evidence/.template/G{N}/README.md`

### 4. Handoff to CEO (§2.5)
- [ ] Push branch and open PR
- [ ] Update `docs/state/progress.md` with "Ready for CEO review"
- [ ] Create session log: `docs/state/SESSIONS/{DATE}_DEV_{TASK}.md`
- [ ] Clear resolved blockers in `docs/state/blockers.md`

---

## Dos and Don'ts

### ✅ Do
- Read VISION.md before starting any task
- Build Phase A + Phase B together
- Write tests (≥80% backend, ≥70% frontend coverage)
- Use types everywhere
- Document complex logic
- Test Owner workflows
- Produce evidence for ALL gates in scope
- Ask questions early

### ❌ Don't
- Build backend without UI
- Use stubs/mocks in production code
- Skip tests ("we'll add them later")
- Hardcode secrets
- Assume Owner is technical
- Build features not in VISION.md
- Ignore quality gates
- Submit without evidence

---

## Common Patterns

### Parallel Agent Execution
```python
def route_to_parallel_agents(state):
    return ["frontend_dev", "backend_dev", "database_engineer"]

workflow.add_conditional_edges(
    "planner",
    route_to_parallel_agents,
    {
        "frontend_dev": "frontend_dev",
        "backend_dev": "backend_dev",
        "database_engineer": "database_engineer"
    }
)
```

### Conditional Routing
```python
def should_retry(state: AgentState) -> str:
    if state["test_results"]["passed"]:
        return "deploy"
    elif state.get("retry_count", 0) < 3:
        return "fix_code"
    return "escalate"
```

### Streaming Progress
```python
async for event in graph.astream_events(initial_state, config):
    if event["event"] == "on_chain_start":
        # Send progress update to frontend
        yield {"type": "progress", "node": event["name"]}
```

---

## Resources

### Constitution (Read in Order)
1. **`constitution/VISION.md`** - What we're building (2 min)
2. **`constitution/STRATEGY.md`** - How we win (5 min)
3. **`constitution/ROADMAP_SPEC.md`** - What ships when (3 min)
4. **`constitution/EXECUTION_PROTOCOL_SPEC.md`** - How to execute tasks (10 min)
5. **`constitution/NOVEMBER_2025_STANDARDS.md`** - Tool versions & thresholds (15 min)
6. **`constitution/STATE_MANAGEMENT.md`** - Living documents protocol (10 min)

###