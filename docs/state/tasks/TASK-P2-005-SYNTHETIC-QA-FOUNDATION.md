# TASK-P2-005-SYNTHETIC-QA-FOUNDATION: Synthetic User QA Engine (MVP)

**Priority**: 🔴 **HIGH** (Phase 2 Main Work)  
**Phase**: Phase 2 - Synthetic User QA  
**Estimated**: 2-3 weeks  
**Gates in Scope**: G1 (Research), G2 (Architecture), G4 (Code Quality), G5 (Tests), G10 (Owner Validation)

---

## ⚠️ CRITICAL: NATIVE FIRST MANDATE

**Before writing ANY custom code, you MUST**:
1. Search LangGraph docs for native capabilities
2. Document native options in `evidence/G1/native_research.md`
3. Justify custom code ONLY if native doesn't exist or is inferior
4. Get CEO approval if building custom solution

---

## Objective

Build MVP Synthetic User QA engine that uses LangGraph native capabilities to:
- Execute one happy-path flow (submit task → check result)
- Generate test plan from requirements
- Control browser via tool integration
- Capture screenshots and pass/fail status
- Block production toggle if tests fail

**From ROADMAP_SPEC.md** (Phase 2): "Synthetic users execute at least one happy-path flow and one error-path flow, producing click-level trace, screenshots, and structured bug reports."

---

## LangGraph Native Capabilities (VERIFIED via MCP)

### ✅ Available Native Features:

**1. Playwright Integration** ([docs.langchain.com](https://docs.langchain.com/oss/python/integrations/providers/microsoft))
- `PlayWrightBrowserToolkit` - Native LangChain integration
- Browser control (Chromium, Firefox, WebKit)
- NOT custom code - use existing toolkit

**2. Human-in-the-Loop** ([docs.langchain.com/oss/python/deepagents/human-in-the-loop))
- `interrupt()` function for approval gates
- Native LangGraph capability
- Saves state, waits for resume with `Command`

**3. Checkpointing & Persistence** ([docs.langchain.com/oss/python/langgraph/persistence))
- `AsyncPostgresSaver` (already in use)
- Automatic state persistence
- Thread-based memory across runs

**4. Custom Streaming Events** ([docs.langchain.com/oss/javascript/langgraph/streaming))
- `get_stream_writer()` (already in use)
- Stream test progress to frontend
- Native event system

**5. Tool Execution** ([docs.langchain.com/langsmith/use-tools))
- Custom tools for executing commands
- LangGraph `ToolNode` pattern
- Structured tool calling

---

## Architecture (Native LangGraph Pattern)

### New Nodes (Add to existing graph):

**1. `test_planner_node`**:
- Input: `state["task"]`, `state["result"]` (from executor)
- LLM generates test plan: "Submit task 'X' → Check result page shows success"
- Output: `test_plan: dict` with steps

**2. `test_executor_node`** (ToolNode):
- Uses **PlayWrightBrowserToolkit** (native)
- Executes test plan steps
- Captures screenshots at each step
- Output: `test_results: dict`, `screenshots: list[str]`

**3. `test_evaluator_node`**:
- Input: `test_results`
- LLM evaluates pass/fail
- Output: `tests_passed: bool`, `test_report: str`

### Graph Flow (Extends existing):

```
executor_node → test_planner_node → test_executor_node → test_evaluator_node → conditional_edge
                                                                                      ↓
                                              IF tests_passed: → production_approval_node (human interrupt)
                                              IF tests_failed:  → bug_report_node → END
```

### State Schema (Additive):

```python
class AgentState(TypedDict):
    # Existing fields...
    schema_version: Literal["1"]
    task: str
    plan: str
    result: str
    messages: list[BaseMessage]
    
    # NEW fields (Phase 2):
    test_plan: dict  # {"steps": [{"action": "click", "selector": "#submit"}]}
    test_results: dict  # {"passed": bool, "screenshots": [...]}
    tests_passed: bool
    test_report: str
```

---

## Phase A: Research (G1) - 3 days

**Deliverable**: `evidence/G1/native_research.md`

**Tasks**:
1. Install and test `PlayWrightBrowserToolkit`:
   ```bash
   pip install langchain-community playwright
   playwright install chromium
   ```

2. Create proof-of-concept:
   - Simple LangChain agent with Playwright tools
   - Navigate to http://localhost:3000
   - Click submit button
   - Capture screenshot

3. Document findings:
   - Does toolkit meet requirements?
   - Any limitations?
   - Alternative: custom Playwright integration?

4. Get CEO approval on approach

---

## Phase B: Backend Implementation (G2, G4, G5) - 1 week

### B1: Create Test Planner Node (2 days)

**File**: `apps/agent-runtime/src/agent_runtime/graph/nodes/test_planner.py`

```python
from langchain_core.messages import HumanMessage
from ...schemas.state import AgentState
from ..graph import get_llm

async def test_planner_node(state: AgentState) -> dict:
    """Generate test plan from task description."""
    llm = get_llm()
    
    prompt = f"""
    Task: {state['task']}
    Result: {state.get('result', 'N/A')}
    
    Generate a simple test plan with one happy-path flow.
    Format: JSON with steps: [{{"action": "navigate", "url": "..."}}, ...]
    """
    
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    test_plan = parse_test_plan(response.content)
    
    return {"test_plan": test_plan}
```

### B2: Create Test Executor Node (3 days)

**File**: `apps/agent-runtime/src/agent_runtime/graph/nodes/test_executor.py`

```python
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents import create_tool_calling_agent

async def test_executor_node(state: AgentState) -> dict:
    """Execute test plan using Playwright."""
    toolkit = PlayWrightBrowserToolkit.from_browser_sync()
    tools = toolkit.get_tools()
    
    # Execute each step in test_plan
    results = []
    for step in state["test_plan"]["steps"]:
        # Use Playwright tools to execute step
        result = await execute_step(step, tools)
        results.append(result)
    
    return {
        "test_results": {"steps": results},
        "screenshots": save_screenshots(results)
    }
```

### B3: Create Test Evaluator Node (1 day)

**File**: `apps/agent-runtime/src/agent_runtime/graph/nodes/test_evaluator.py`

```python
async def test_evaluator_node(state: AgentState) -> dict:
    """Evaluate test results."""
    test_results = state["test_results"]
    
    # Check if all steps passed
    tests_passed = all(step.get("passed") for step in test_results["steps"])
    
    # Generate report
    report = generate_test_report(test_results)
    
    return {
        "tests_passed": tests_passed,
        "test_report": report
    }
```

### B4: Update Graph (1 day)

**File**: `apps/agent-runtime/src/agent_runtime/graph/graph.py`

```python
# Import new nodes
from .nodes.test_planner import test_planner_node
from .nodes.test_executor import test_executor_node
from .nodes.test_evaluator import test_evaluator_node

def create_graph(checkpointer):
    workflow = StateGraph(AgentState)
    
    # Add new nodes
    workflow.add_node("test_planner", test_planner_node)
    workflow.add_node("test_executor", test_executor_node)
    workflow.add_node("test_evaluator", test_evaluator_node)
    
    # Update flow
    workflow.add_edge("executor", "test_planner")
    workflow.add_edge("test_planner", "test_executor")
    workflow.add_edge("test_executor", "test_evaluator")
    workflow.add_conditional_edges(
        "test_evaluator",
        lambda state: "approve" if state["tests_passed"] else "fail",
        {
            "approve": "production_interrupt",
            "fail": END
        }
    )
```

---

## Phase C: Frontend UI (G10) - 3 days

### C1: QA Results View

**File**: `apps/web/src/app/qa-results.tsx`

```tsx
export function QAResults({ testReport, screenshots }) {
  return (
    <div className="qa-results">
      <h2>Synthetic QA Results</h2>
      
      <div className="test-report">
        {testReport.steps.map(step => (
          <div key={step.id}>
            <span>{step.passed ? '✅' : '❌'}</span>
            <span>{step.description}</span>
          </div>
        ))}
      </div>
      
      <div className="screenshots">
        {screenshots.map(img => (
          <img key={img} src={img} alt="Test screenshot" />
        ))}
      </div>
    </div>
  );
}
```

### C2: Integrate with Production Toggle

Update existing UI to show QA status before production approval.

---

## Success Criteria (CLAUDE.md Rules)

### ✅ Rule 1: Phase A + Phase B Together
- ✅ Backend: 3 new LangGraph nodes
- ✅ Frontend: QA results view in Owner Console

### ✅ Rule 2: Docker from Line 1
- ✅ Playwright in Docker: `Dockerfile` updated with `playwright install`
- ✅ Test in Docker: `docker-compose exec agent-runtime pytest tests/test_synthetic_qa.py`
- ✅ Owner validation: View QA results in browser at `localhost:3000`

### ✅ Rule 3: Evidence-Based Approval
**Required Evidence**:
1. `evidence/G1/native_research.md` - Playwright POC
2. `evidence/G2/architecture.md` - Node diagrams
3. `evidence/G4/lint_type_output.txt` - Clean code
4. `evidence/G5/test_coverage.txt` - ≥85% coverage
5. `evidence/G10/owner_validation_screenshots/` - Owner testing screenshots
6. Docker logs showing successful test execution

### ✅ GOLDEN_RULES Coverage 85%
- Unit tests for each new node
- Integration test: Full happy-path flow
- Total: ≥85% line coverage (G5 requirement)

---

## Owner Validation (≤20 min)

**Steps**:
1. Start Docker: `docker-compose up -d`
2. Navigate to `http://localhost:3000`
3. Submit test task: "Build a todo app"
4. Observe:
   - Task executes
   - Synthetic QA runs automatically
   - Screenshots appear in UI
   - Test report shows pass/fail
   - Production toggle blocked if tests fail

**Owner submits**:
- 3 screenshots: (1) Task submitted, (2) QA running, (3) QA results
- Docker logs: `docker-compose logs agent-runtime | grep synthetic_qa`

---

## Risks & Mitigations

**Risk 1**: Playwright flaky in Docker  
**Mitigation**: Use headless mode, stable selectors

**Risk 2**: Complex test plans overwhelm MVP  
**Mitigation**: Start with ONE simple test (submit → check result)

**Risk 3**: Screenshot storage fills disk  
**Mitigation**: Limit to 5 screenshots per test, auto-delete old runs

---

## Next Task After Completion

**TASK-P2-006**: Add error-path testing (happy + sad paths)
