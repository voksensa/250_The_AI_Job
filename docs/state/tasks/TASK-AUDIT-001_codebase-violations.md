# TASK-AUDIT-001: Complete Codebase Violation Audit

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: CRITICAL  
**Date**: 2025-11-21  
**Estimated Effort**: 4-6 hours  

---

## Objective

Audit **ALL files** in the codebase to identify violations of core principles:
1. **"Production from Line 1"** - No mocks, stubs, TODOs, dummy data, placeholders
2. **"Native over Custom"** - No custom implementations when native LangGraph/library solutions exist
3. **Evidence-Based Code** - All implementations must reference official docs/specs, not generic patterns
4. **Consistency** - No contradictions between constitution files, manuals, and code

---

## Your Role

1. **Validate CEO's initial findings** (will be provided)
2. **Catch violations CEO missed** (he's incompetent at execution)
3. **Use official LangGraph 1.0.3 docs** via MCP tool to verify all graph/agent code is native
4. **Compile actionable report** with specific line numbers, evidence, and recommended fixes

---

## Scope

### Files to Audit (ALL)

**Constitution:**
- `constitution/VISION.md`
- `constitution/ROADMAP_SPEC.md`
- `constitution/EXECUTION_PROTOCOL_SPEC.md`
- `constitution/NOVEMBER_2025_STANDARDS.md`
- `constitution/ENGINE_ARCHITECTURE_V1.md`
- `constitution/STATE_MANAGEMENT.md`

**Manuals:**
- `CLAUDE.md`
- `AGENTS.md`

**Code:**
- `apps/agent-runtime/src/**/*.py` (all Python files)
- `apps/web/src/**/*.{ts,tsx}` (all TypeScript/React files)
- `apps/agent-runtime/pyproject.toml`
- `apps/web/package.json`

**Evidence/Templates:**
- `evidence/.template/G*/README.md` (all gate templates)
- `evidence/.template/G*/TEMPLATE-*.md`

**State/Docs:**
- `docs/state/*.md`
- `docs/research/*.md`

**Config:**
- `.github/workflows/*` (if exists)
- `docker-compose.yml`
- `Dockerfile` (any)
- `apps/agent-runtime/ruff.toml`
- `apps/web/vitest.config.ts`

---

## Violation Categories to Find

### 1. Mock/Stub/Placeholder Violations

**Search for these patterns:**
- Language: "dummy", "mock", "stub", "placeholder", "fake", "simple", "minimal", "TODO", "FIXME", "sample"
- Code patterns: `# TODO:`, `// TODO:`, mock data, hardcoded test values outside actual tests
- Ideology: "start simple then harden", "prototype first", "MVP then production"

**Principle**: Every build from character 1 must be production-grade. Even validation builds must solve real problems with real infra.

**Examples of violations:**
```python
# BAD - Mock/Placeholder
database_url = "sqlite:///:memory:"  # TODO: use real Postgres
llm = MockLLM()  # placeholder for testing

# GOOD - Real from line 1
database_url = settings.postgres_url  # Real Postgres, configured
llm = ChatAnthropic(model="claude-4.5-sonnet")  # Real LLM
```

### 2. Custom Code When Native Exists

**Focus areas:**
- LangGraph state management (must use PostgresSaver, not custom/MemorySaver)
- Streaming (must use `astream`, `get_stream_writer` - NO custom broadcast)
- Agent patterns (must use LangGraph 1.0.3 native patterns)
- Checkpointing (must use `langgraph-checkpoint-postgres 3.0.x`)

**How to verify:**
Use the `mcp0_SearchDocsByLangChain` tool to query official docs:

```python
# Example queries to run:
mcp0_SearchDocsByLangChain(query="PostgresSaver checkpointer langgraph 1.0")
mcp0_SearchDocsByLangChain(query="astream streaming events langgraph")
mcp0_SearchDocsByLangChain(query="get_stream_writer custom events")
mcp0_SearchDocsByLangChain(query="langgraph interrupt human approval")
```

**Report format:**
```
VIOLATION: apps/agent-runtime/src/agent_runtime/graph.py:45-67
Type: Custom code when native exists
Found: Custom WebSocket manager for streaming
Native alternative: LangGraph `astream` with `stream_mode=["updates", "custom"]`
Evidence: [link to LangChain docs from MCP query]
Recommendation: Replace custom manager with native streaming
```

### 3. Non-Evidence-Based Generic Code

**Look for:**
- Generic REST patterns not aligned with FastAPI best practices
- Generic React patterns not aligned with Next.js 16 App Router
- Generic suggestions like "use Redis" without evidence for why
- Unsubstantiated claims (e.g., "this is faster" without benchmarks)

**Verification:**
- Cross-reference with `NOVEMBER_2025_STANDARDS.md` §2 for tool versions
- Cross-reference with `ENGINE_ARCHITECTURE_V1.md` for stack decisions
- All architectural choices must cite spec sections or external evidence

### 4. Contradictions Between Files

**Check for:**
- ROADMAP_SPEC.md saying "Phase 0: dummy pipeline" vs AGENTS.md saying "production from line 1"
- CLAUDE.md quality gates vs EXECUTION_PROTOCOL evidence requirements (must align)
- Tool versions in NOVEMBER_2025_STANDARDS.md vs actual pyproject.toml/package.json
- State management conventions in STATE_MANAGEMENT.md vs actual docs/state/ files

**Report conflicting statements:**
```
CONTRADICTION: 
File A: constitution/ROADMAP_SPEC.md:245
Says: "Start with minimal but strict subset of gates (G1-G5)"
File B: CLAUDE.md:38
Says: "Every deliverable must pass ALL gates (G1-G11)"
Resolution needed: Clarify which gates apply to which phases
```

---

## Tools You Must Use

### 1. MCP LangChain Docs Tool

```bash
# In your agent environment, you have access to:
mcp0_SearchDocsByLangChain(query="your search query")

# This queries the OFFICIAL LangChain/LangGraph docs
# Use it to verify every LangGraph pattern in the codebase
```

**Key queries to run:**
1. "langgraph 1.0.3 checkpointer postgres"
2. "langgraph streaming astream custom events"
3. "langgraph interrupt human in the loop"
4. "langgraph state annotation typed dict"
5. "langgraph conditional edges routing"
6. "langgraph-checkpoint-postgres 3.0 setup"

### 2. Code Search Tools

Use `grep_search` and `codebase_search` to find patterns:
```bash
# Examples:
grep_search(Query="TODO", SearchPath="apps/")
grep_search(Query="dummy", SearchPath="constitution/")
grep_search(Query="mock", SearchPath="apps/agent-runtime/src/")
codebase_search(Query="custom websocket manager", TargetDirectories=["apps/agent-runtime"])
```

---

## Deliverable: Audit Report

Create: `/Users/Yousef_1/.gemini/antigravity/brain/.../audit_report.md`

### Structure:

```markdown
# Codebase Violation Audit Report

**Date**: 2025-11-21  
**Auditor**: Developer  
**Reviewed By**: CEO (pending)  

---

## Executive Summary

- Total files audited: [N]
- Total violations found: [N]
- Critical violations (blocking): [N]
- Medium violations (should fix): [N]
- Low violations (cleanup): [N]

---

## Critical Violations (MUST FIX)

### V-001: [Short description]
- **File**: [path:line]
- **Type**: [Mock/Custom/Contradiction/Generic]
- **Found**: [exact quote or code snippet]
- **Violation**: [why this violates principles]
- **Evidence**: [link to spec/docs that proves violation]
- **Fix**: [specific action to take]

[Repeat for each critical violation]

---

## Medium Violations (SHOULD FIX)

[Same structure]

---

## Low Violations (CLEANUP)

[Same structure]

---

## LangGraph Native Verification

### Queries Run
1. Query: "PostgresSaver checkpointer"
   Result: [summary]
   Code Status: [compliant/non-compliant]

[For each query]

---

## Contradictions Matrix

| File A | Line | Says | File B | Line | Says | Resolution |
|--------|------|------|--------|------|------|------------|
| ... | ... | ... | ... | ... | ... | ... |

---

## CEO Findings Validation

CEO provided [N] initial findings. Developer validation:
- Confirmed: [N]
- False positives: [N] 
- Additional violations CEO missed: [N]

[List what CEO missed]

---

## Recommendations

### Immediate Actions (before Phase 1)
1. [Action with rationale]
2. [Action with rationale]

### Systematic Fixes
1. [Pattern to change across codebase]
2. [Process improvement]

---

## Evidence Attached

- [Links to MCP query results]
- [Links to relevant spec sections]
- [Code snippets/diffs if helpful]
```

---

## Success Criteria

- [ ] ALL files in scope audited
- [ ] Every LangGraph pattern verified against official 1.0.3 docs via MCP
- [ ] At least 10 LangChain doc queries run and documented
- [ ] All "dummy/mock/stub/TODO" patterns flagged
- [ ] All contradictions between constitution files identified
- [ ] Report includes line numbers and evidence for every violation
- [ ] Specific, actionable fixes proposed for critical violations
- [ ] CEO findings validated (confirmed or corrected)

---

## CEO's Initial Findings (For Developer Validation)

**Date**: 2025-11-21  
**Method**: Automated grep searches + manual review  
**Total findings**: 8 violations identified  

---

### CRITICAL VIOLATIONS (Must Fix Before Phase 1)

#### V-CEO-001: "Dummy Build Pipeline" in Phase 0 Validation

**File**: `constitution/ROADMAP_SPEC.md:202-203`  
**Type**: Mock/Placeholder Violation  
**Found**:
```
* Executes a dummy build pipeline.
* Produces a minimal app artifact.
```

**Violation**: Directly contradicts "Production from Line 1" principle. Even Phase 0 validation must build a **real production app** (e.g., working todo list with auth, DB, tests), not a dummy/minimal placeholder.

**Evidence**: 
- AGENTS.md:26: "No stubs, no mocks, no 'TODO: implement later'"
- CLAUDE.md:79: "Mocks ('this simulates the real thing')" listed as FORBIDDEN

**Fix Required**: Replace with:
```
* Executes a complete build of a real starter app (e.g., authenticated todo list with Postgres, deployed to real Docker)
* Produces a production-grade app with:
  - Real LLM calls
  - Real database (Postgres, not SQLite memory)
  - Real tests (≥80% backend coverage)
  - Real deployment (Docker container)
```

**Developer Action**: 
1. Confirm this is a violation
2. Rewrite ROADMAP_SPEC.md Phase 0 "Owner Validation" section lines 197-208
3. Ensure alignment with ENGINE_ARCHITECTURE_V1.md (if exists)

---

#### V-CEO-002: "Minimal App Artifact" Language

**File**: `constitution/ROADMAP_SPEC.md:203`  
**Type**: Mock/Placeholder Violation  
**Found**: "Produces a minimal app artifact"

**Violation**: "Minimal" suggests incomplete/placeholder. Must be "production-grade starter app."

**Fix**: Change to "Produces a production-grade starter app artifact"

---

#### V-CEO-003: "Minimal Build Story" Language

**File**: `constitution/ROADMAP_SPEC.md:243`  
**Type**: Mock/Placeholder Violation  
**Found**: "Inspect a minimal build story (what was built, which tests ran)"

**Violation**: Same as V-CEO-002. Build story must be complete, not minimal.

**Fix**: "Inspect a complete build story showing requirements, architecture, tests, and deployment"

---

#### V-CEO-004: "Minimal but Strict Subset" Contradiction

**File**: `constitution/ROADMAP_SPEC.md:220`  
**Type**: Contradiction  
**Found**: "Start with a minimal but strict subset of gates (G1–G5) in P0"

**Violation**: Contradicts CLAUDE.md which states "Every deliverable must pass ALL gates (G1-G11)"

**Cross-reference**:
- CLAUDE.md likely says all gates required
- This creates ambiguity on which gates apply to which phases

**Developer Action**:
1. Check CLAUDE.md for exact gate requirements
2. Check EXECUTION_PROTOCOL_SPEC.md for per-phase gate mapping
3. Either:
   - Clarify that Phase 0 only requires G1-G5 (update CLAUDE.md)
   - OR require all gates from Phase 0 (update ROADMAP_SPEC.md)
4. Document decision in DECISIONS_LOG.md

---

### MEDIUM VIOLATIONS (Should Fix)

#### V-CEO-005: "Prototype Mode" with "Minimal Testing"

**File**: `constitution/STRATEGY.md:41`  
**Type**: Mock/Placeholder Violation  
**Found**: "**Prototype Mode**: Fast, cheap, minimal testing (2-5 minutes)"

**Violation**: "Minimal testing" violates quality standards. Even prototype mode must meet coverage thresholds.

**Fix**: Clarify that prototype mode still requires:
- Lint clean
- Tests passing
- Minimum coverage (specify threshold, e.g., ≥60%)
- Difference is speed/scope, not quality

---

#### V-CEO-006: "Simple Subset" and "Basic Example" Language

**File**: Multiple instances across ROADMAP_SPEC.md  
**Type**: Generic/Vague Language  
**Found**:
- Line 381: "Start with a small, stable set of tasks"
- Line 233: "simple funnel"
- Line 286: "basic CRUD works"

**Violation**: "Simple/basic/small" without specifications can lead to cutting corners.

**Fix**: Define what "simple" means with concrete criteria:
- "Starter set: login, main CRUD flow, logout"
- "Basic CRUD: Create/Read/Update/Delete with validation and error handling"

---

### LOW VIOLATIONS (Cleanup/Clarification)

#### V-CEO-007: "Minimal Documentation" in STATE_MANAGEMENT

**File**: `constitution/STATE_MANAGEMENT.md:766`  
**Type**: Contradictory Guidance  
**Found**: "Only minimal docs; lean on code and chat."

**Violation**: Listed as an anti-pattern (DocsLevel: Sparse Documentation) but the word "minimal" appears as guidance.

**Fix**: Clarify this is describing what NOT to do, or remove ambiguous language.

---

#### V-CEO-008: Missing LangGraph Native Verification

**File**: Codebase (Python files)  
**Type**: Potential Custom Code  
**Status**: NEEDS DEVELOPER VERIFICATION

**Concern**: Did not find `graph.py` in expected location. Need to verify:
1. Does LangGraph code exist?
2. If yes, does it use:
   - PostgresSaver (not MemorySaver)?
   - Native `astream` (not custom streaming)?
   - Native `get_stream_writer` (not custom broadcast)?
3. All patterns must be verified against official LangChain docs via MCP

**Developer Action**: 
1. Locate all LangGraph implementation files
2. Run MCP queries to verify each pattern is native
3. Document findings in audit report

---

## Notes

- **Be thorough**: CEO admitted he's bad at execution - catch what he missed
- **Be precise**: Line numbers, exact quotes, evidence links required
- **Be actionable**: Every violation must have a clear fix
- **Use MCP tool**: Official docs are the source of truth, not generic patterns
- **No mercy**: If it violates "production from line 1" or "native over custom", flag it

---

## Timeline

- **Start**: Immediately after CEO appends initial findings
- **Duration**: 4-6 hours focused work
- **Delivery**: Completed audit report for CEO review
