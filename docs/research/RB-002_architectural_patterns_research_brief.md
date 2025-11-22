# RESEARCH BRIEF: Architectural Patterns That Become Exponentially Expensive to Change

**Research ID**: RB-002  
**Date**: 2025-11-22  
**Requesting Authority**: Owner (via CEO)  
**Assigned To**: External Researcher (RESEARCH_BRIEF_EXECUTION_FRAMEWORK)  
**Priority**: 🔴 CRITICAL - BLOCKS TASK-P1-002  
**Deadline**: Within 24 hours (blocks development)

---

## Executive Summary

**Problem**: We are building an AI agent system where developer agents have 15-20 minute memory windows (context resets). We need to identify which architectural patterns MUST be established NOW versus which can be safely deferred to later phases.

**Why This Matters**: Some architectural decisions (API versioning, error schemas, state structures) become exponentially more expensive to change after code is written because:
1. Agent memory resets = inconsistent application of patterns
2. Breaking changes require refactoring all existing code
3. Database/state schema changes cascade through entire system

**Your Mission**: Provide evidence-based determination of which architectural patterns have high "cost of change later" and must be enforced in Phase 1.

---

## Context

### Current State
- **Phase**: Phase 1 MVP (Production Toggle)
- **Active Task**: TASK-P1-002 (Production Toggle Switch implementation)
- **Tech Stack**: 
  - Backend: FastAPI, LangGraph 1.0.3, PostgreSQL
  - Frontend: Next.js 15, React, TypeScript
  - Agent Memory: 15-20 minute context window (goldfish memory)

### Key Constraint
**Agent Memory Persistence Problem**: Developer agents reset context every 15-20 minutes. Without clear documented patterns, agents will:
- Create inconsistent API endpoints (`/api/tasks` vs `/api/v1/tasks`)
- Use different error response formats
- Place files in random locations
- Mix naming conventions

---

## Research Questions

### RQ1: API Design Patterns (Versioning)
**Question**: Must API versioning strategy be established in Phase 1, or can it be added later without breaking changes?

**Context**: Current API endpoints:
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `WebSocket /api/tasks/{id}/stream`

**Specific Sub-Questions**:
1. What is the industry-standard versioning approach for REST APIs in November 2025?
2. What is the cost of migrating unversioned → versioned APIs after production deployment?
3. Does URI path versioning (`/api/v1/`) have advantages over header-based versioning for agent memory persistence?
4. Can versioning be added retroactively without breaking existing clients?

**Evidence Required**:
- Official API design guidelines (Google, Microsoft, Stripe, Twilio)
- Case studies of API versioning migrations
- November 2025 best practices from authoritative sources (min 3)

---

### RQ2: Error Response Standardization
**Question**: Must error response format be standardized NOW, or can it evolve organically?

**Context**: Current error responses are inconsistent:
- FastAPI default: `{"detail": "Not Found"}`
- Custom errors: Various formats

**Specific Sub-Questions**:
1. What is the RFC 9457 (Problem Details) standard for HTTP error responses?
2. Is RFC 9457 the November 2025 industry standard, or is there a newer alternative?
3. What is the cost of migrating from ad-hoc error responses to standardized format?
4. Will agent memory resets cause error format drift if not documented strictly?

**Evidence Required**:
- RFC 9457 specification review
- Industry adoption (GitHub, Stripe, AWS, Azure error formats)
- November 2025 best practices (min 3 sources)

---

### RQ3: LangGraph State Schema Evolution
**Question**: What patterns prevent breaking changes when extending LangGraph state schemas?

**Context**: Current state structure:
```python
class AgentState(TypedDict):
    messages: List[BaseMessage]
    task: str
    plan: str
    result: str
```

**Specific Sub-Questions**:
1. How do LangGraph checkpointers (PostgresSaver) handle schema changes?
2. What is the equivalent of "database migration" for LangGraph state?
3. Can fields be added/removed without breaking existing checkpoint data?
4. What are the November 2025 best practices for versioned state schemas?

**Evidence Required**:
- LangGraph 1.0.3 official documentation on state evolution
- TypedDict extension patterns (PEP 589, PEP 655)
- Case studies from LangGraph or similar state machine migrations

---

### RQ4: Codebase Structure Conventions
**Question**: Which file/folder organization patterns reduce agent confusion and technical debt?

**Context**: Current structure:
```
apps/agent-runtime/src/agent_runtime/
├── api/routes.py
├── graph.py
├── main.py
└── settings.py
```

**Specific Sub-Questions**:
1. What is the November 2025 standard for Python monorepo package structure?
2. Where should new LangGraph nodes be placed (`/nodes/`, `/graph/nodes/`, flat)?
3. What conventions prevent "utility file sprawl" (`utils.py`, `helpers.py`, `common.py`)?
4. How do large Python projects (Django, FastAPI, Airflow) organize similar structures?

**Evidence Required**:
- Python Packaging Authority (PyPA) guidelines
- Real-world examples from open-source projects (FastAPI, LangChain, Airflow)
- November 2025 best practices for monorepo structure

---

### RQ5: Naming Convention Enforcement
**Question**: Must naming conventions be enforced across boundaries (Python/TypeScript/JSON) NOW?

**Context**: Current inconsistency risk:
- Python: `snake_case` (PEP 8)
- TypeScript: `camelCase` or `snake_case`?
- JSON API responses: `snake_case` or `camelCase`?
- Database columns: unclear

**Specific Sub-Questions**:
1. What is the November 2025 standard for JSON API field naming?
2. Do modern frameworks (FastAPI, Next.js) auto-convert between conventions?
3. What is the cost of migrating API responses from `camelCase` → `snake_case`?
4. How do agent memory resets affect consistency if conventions aren't documented?

**Evidence Required**:
- Google JSON Style Guide
- Stripe, Twilio, AWS API naming conventions
- FastAPI/Pydantic serialization best practices

---

### RQ6: Import Path Standards
**Question**: Do import path inconsistencies (relative vs absolute) cause technical debt?

**Context**: Current mixed usage:
```python
from .api.routes import router  # Relative
from agent_runtime.graph import create_graph  # Absolute
```

**Specific Sub-Questions**:
1. What does PEP 8 recommend for relative vs absolute imports?
2. Do modern type checkers (mypy, Pyright) prefer one style?
3. What is the refactoring cost of standardizing imports later?
4. Does mixing styles cause agent confusion in larger codebases?

**Evidence Required**:
- PEP 8 official guidelines
- mypy documentation on import resolution
- Real-world examples from large Python projects

---

## CEO Preliminary Findings (UNVALIDATED - For Reference Only)

**IMPORTANT**: The following are CEO hypotheses based on preliminary web search. **These are NOT evidence and must be independently verified by researcher.**

### Hypothesis 1: API Versioning is Cheap to Add, Expensive to Migrate
- **Claim**: URI path versioning (`/api/v1/`) costs ~10 minutes now vs ~2+ hours later
- **Sources**: Web search (unverified)
- **Status**: ⚠️ NEEDS VALIDATION

### Hypothesis 2: Error Format Standardization Prevents Cascading Fixes
- **Claim**: RFC 9457 is the November 2025 standard
- **Sources**: Web search (unverified)
- **Status**: ⚠️ NEEDS VALIDATION

### Hypothesis 3: LangGraph State is Like Database Schema
- **Claim**: State changes require migrations like databases
- **Sources**: LangChain docs (preliminary MCP search)
- **Status**: ⚠️ NEEDS VALIDATION

### Hypothesis 4-6: File Structure, Naming, Imports
- **Claims**: Various conventions reduce agent confusion
- **Sources**: General web search
- **Status**: ⚠️ ALL NEED VALIDATION

**Researcher must validate or refute each hypothesis with authoritative November 2025 sources.**

---

## Success Criteria

### Minimum Evidence Standard
For each research question, provide:

1. **Primary Sources** (min 2):
   - Official documentation (Python, TypeScript, FastAPI, LangGraph)
   - RFC specifications where applicable
   - Authoritative vendor guidelines (Google, Microsoft, Stripe)

2. **Real-World Examples** (min 1):
   - Open-source project demonstrating pattern
   - Case study of migration/refactoring cost
   - Industry benchmark data

3. **November 2025 Currency**:
   - All sources must be current as of Nov 2025 or explicitly noted as "stable standard"
   - Deprecated/outdated practices must be flagged

4. **Agent Memory Context**:
   - Explicitly address: "Does pattern X prevent agent confusion with 15-20min memory?"
   - Provide clear yes/no answer with justification

---

## Deliverables

### Required Document
`docs/research/RB-002_architectural_patterns_cost_of_change.md`

**Structure**:
```markdown
# Research Brief RB-002: Architectural Patterns Cost of Change

## Executive Summary
[One paragraph: What patterns MUST be enforced NOW vs deferred]

## RQ1: API Versioning
### Finding: [Enforce NOW | Safe to Defer | Conditional]
### Evidence:
- [Source 1]: [URL] - [Key Finding]
- [Source 2]: [URL] - [Key Finding]
- [Example]: [Real-world case]
### November 2025 Best Practice:
[Clear statement of current standard]
### Agent Memory Impact:
[How pattern prevents agent confusion]
### CEO Hypothesis Validation:
[VALIDATED | REFUTED | PARTIALLY VALIDATED]

[Repeat for RQ2-RQ6]

## Decision Matrix
| Pattern | Enforce Phase | Cost if Deferred | Evidence Weight |
|---------|---------------|------------------|-----------------|
| API Versioning | 1 / 2 / 3 | Low/Med/High | Strong/Weak |
| ... | ... | ... | ... |

## Recommendations
1. **MUST ENFORCE NOW**: [List with justification]
2. **SAFE TO DEFER**: [List with justification]
3. **CONDITIONAL**: [List with conditions]

## References
[Full bibliography in APA format]
```

---

## Timeline

**Start**: Immediately upon receipt  
**Duration**: 12-24 hours (time-boxed)  
**Deadline**: 2025-11-23 18:00 CET

**Checkpoints**:
- **6 hours**: Interim findings on RQ1-RQ2 (highest priority)
- **12 hours**: Draft decision matrix
- **24 hours**: Final report with all evidence

---

## Constraints

### What Researcher Should NOT Do
1. ❌ Rely on CEO preliminary findings as evidence
2. ❌ Use generic "best practices" without November 2025 verification
3. ❌ Skip real-world examples
4. ❌ Provide opinions without source citations

### What Researcher MUST Do
1. ✅ Cite all sources with URLs
2. ✅ Validate November 2025 currency
3. ✅ Provide clear "Enforce NOW" vs "Defer" recommendations
4. ✅ Include agent memory impact analysis
5. ✅ Verify or refute CEO hypotheses explicitly

---

## Impact if Research is Incomplete

**If we guess wrong**:
- Enforce too early → Wasted effort, over-engineering
- Defer too late → 10-100x refactoring cost, broken production

**If we rely on unvalidated findings**:
- Agent applies inconsistent patterns
- Technical debt accumulates exponentially
- Phase 2+ delivery blocked by Phase 1 refactoring

**This research is the foundation for all Phase 1+ architectural decisions.**

---

## Questions for Researcher

If anything is unclear:
1. Scope ambiguous?
2. Need access to specific tools/APIs?
3. Timeline constraints?
4. Additional context needed?

**Contact**: CEO (via Owner)

---

**This is a CRITICAL PATH research brief. Phase 1 development is blocked pending findings.**
