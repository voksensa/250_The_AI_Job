# ARCHITECTURAL DECISIONS (Enforced Phase 1)

---

## 🔒 Non-Negotiable Architecture Rules (Applies Everywhere)

**These 5 rules are constitutional law. No exceptions, no deferral.**

1. **Put `/api/v1/` on every backend URL now** so we never have to rename all our APIs later.
2. **Use one standard error shape for all failures** (RFC 9457 Problem Details: same fields, same style) so every part of the system knows how to read errors.
3. **Treat the LangGraph state like a saved form**: only add new fields, don't rename or delete them without a plan, or old runs will break.
4. **Fix folder layout, naming style, and import style now** so AI Developers always see the same patterns and don't invent new ones every 20 minutes.
5. **One naming rule everywhere (snake_case)** for JSON, database, Python, and TypeScript so we never have to rename fields across the whole system later.

> **If this summary and a detailed spec disagree, the detailed spec wins.**  
> This document IS the detailed spec. See also: `docs/research/RB-002_architectural_patterns_cost_of_change.md`

---



---

## Decision Summary

The following 6 architectural patterns have been **validated by external researcher** as having **exponentially high cost of change later**. They MUST be enforced starting in Phase 1 (Production Toggle).

**All CEO hypotheses: VALIDATED**

---

## D1: API Versioning (RB-002-D1)

### Decision
**Adopt explicit path-based versioning `/api/v1/...` from Phase 1 onward.**

### Requirements
- All REST endpoints: `POST /api/v1/tasks`, `GET /api/v1/tasks/{id}`
- All WebSocket endpoints: `WS /api/v1/tasks/{id}/stream`
- **No unversioned endpoints allowed**

### Enforcement
- Router must include version prefix
- Lint check: grep for `/api/` not `/api/v1/`
- Code review required for any new endpoint

### Evidence Weight
**Strong** - Microsoft, Google, Azure all require explicit versioning; retrofitting costs 10-20x

---

## D2: Error Response Format (RB-002-D2)

### Decision
**Standardize all HTTP error responses on RFC 9457 Problem Details.**

### Requirements
All non-200 responses must use:
```json
{
  "type": "https://yfe.app/errors/validation-failed",
  "title": "Validation failed",
  "status": 400,
  "detail": "Missing field 'taskName'.",
  "instance": "urn:trace:9e302a...",
  "errors": { ... }
}
```

### Implementation
- Create `agent_runtime/schemas/api/problem_detail.py`
- FastAPI exception handler wrapping all errors
- **No ad-hoc error formats** (`{"detail": "..."}` forbidden)

### Enforcement
- Shared `ProblemDetail` Pydantic model
- Exception middleware validates format
- API tests verify RFC 9457 compliance

### Evidence Weight
**Strong** - RFC 9457 is 2025 standard; migrating later touches every endpoint + client

---

## D3: LangGraph State Schema (RB-002-D3)

### Decision
**Treat LangGraph state as versioned, additive TypedDict contract with explicit schema_version.**

### Requirements
```python
class AgentState(TypedDict):
    schema_version: Literal["1"]  # REQUIRED
    messages: List[BaseMessage]
    task: str
    plan: str
    result: str
    # New fields MUST be NotRequired or have defaults
    lint_status: NotRequired[str]
    test_status: NotRequired[str]
```

### Rules
1. **Never remove fields** from AgentState
2. **Never rename fields** without migration task
3. **Only add optional fields** (`NotRequired[]` or defaults)
4. **Bump schema_version** for any non-trivial change
5. **Write upgrade function** for version migrations

### Enforcement
- Git pre-commit hook: detect AgentState field removals/renames
- Code review: all state changes require CEO approval
- Session log: document state evolution rationale

### Evidence Weight
**Strong** - LangGraph has no built-in migration; breaking changes invalidate checkpoints

---

## D4: Codebase Layout (RB-002-D4)

### Decision
**Use src/ layout with stable package structure for `agent-runtime`.**

### Required Structure
```
apps/agent-runtime/src/agent_runtime/
├── __init__.py
├── main.py
├── settings.py
├── api/
│   └── routers/
│       ├── tasks.py
│       └── health.py
├── graph/
│   ├── graph.py
│   └── nodes/
│       ├── planning.py
│       ├── building.py
│       ├── testing.py
│       └── production_toggle.py
├── schemas/
│   ├── api/
│   │   └── tasks.py
│   └── state.py
├── services/
│   ├── tasks_service.py
│   └── sandbox_service.py
├── infra/
│   ├── db.py
│   └── checkpointing.py
└── utils/
    └── logging.py
```

### Rules
- **LangGraph nodes**: `graph/nodes/*.py`
- **API routes**: `api/routers/*.py`
- **Utils**: Only for cross-cutting concerns, documented in `utils/README.md`
- **Forbidden**: `common.py`, `helpers.py`, generic filenames

### Enforcement
- File creation must follow structure
- Code review: reject misplaced files
- Document in `CODEBASE_STRUCTURE.md`

### Evidence Weight
**Moderate-Strong** - PyPA recommends src/; prevents file sprawl in AI-dev context

---

## D5: Naming Conventions (RB-002-D5)

### Decision
**Use snake_case for JSON fields, DB columns, Python, and TypeScript models.**

### Requirements
- **JSON API**: `{"task_id": "...", "created_at": "..."}`
- **Python**: `task_id: str`, `created_at: datetime`
- **TypeScript**: `type Task = { task_id: string; created_at: string; }`
- **Database**: `task_id`, `created_at`

### No Conversion Needed
- FastAPI/Pydantic: No alias configuration needed
- TypeScript: Configure ESLint to allow snake_case in API types

### Enforcement
- Lint: ruff checks Python snake_case
- Lint: ESLint custom rule for API types
- Code review: reject camelCase in JSON

### Evidence Weight
**Strong** - Renaming fields across API/DB/clients is highly disruptive

---

## D6: Import Style (RB-002-D6)

### Decision
**Prefer absolute imports within project packages.**

### Requirements
```python
# ✅ CORRECT
from agent_runtime.api.routers.tasks import router
from agent_runtime.graph.graph import create_graph

# ❌ WRONG
from ...api.routers.tasks import router  # Multi-dot relative
```

### Exceptions Allowed
- Single-dot relative within same package:
  ```python
  from .tasks import router  # OK if in same directory
  ```

### Enforcement
- Ruff: Enable `relative-imports` rule
- Code review: flag multi-dot patterns

### Evidence Weight
**Strong** - PEP 8 recommends absolute; easier refactoring + AI clarity

---

## Enforcement Mechanisms

### 1. Documentation
- ✅ This file (`ARCHITECTURAL_DECISIONS.md`)
- Create `CODEBASE_STRUCTURE.md` with layout diagram
- Update `CLAUDE.md` with enforcement protocol

### 2. Linting
```toml
# ruff.toml additions
[lint]
select = [
    "TID252",  # relative-imports
    "N",       # pep8-naming
]
```

### 3. Code Review Checklist
Every PR must verify:
- [ ] API endpoints use `/api/v1/`
- [ ] Errors use `ProblemDetail` model
- [ ] AgentState changes are additive only
- [ ] Files placed in correct package
- [ ] JSON/Python use snake_case
- [ ] Imports are absolute

### 4. CI Checks (Phase 2)
- API version grep check
- Error format validator
- AgentState diff analyzer
- File structure validator

---

## Impact on TASK-P1-002

**Production Toggle Switch implementation MUST comply with all 6 decisions:**

1. Quality gate endpoints: `/api/v1/tasks/{id}/gates`
2. Gate failure errors: RFC 9457 Problem Details
3. AgentState fields: `lint_status`, `test_status` as `NotRequired[str]`
4. Gate nodes: `graph/nodes/lint_gate.py`, `graph/nodes/test_gate.py`
5. Frontend models: `{ lint_status: string, test_status: string }`
6. Imports: Absolute for cross-package references

**Developer implementing P1-002 must read this file before starting.**

---

## References

- Research Brief: `docs/research/RB-002_architectural_patterns_research_brief.md`
- Research Findings: `docs/research/RB-002_architectural_patterns_cost_of_change.md`
- Evidence: `evidence/G1/decisions.json`
