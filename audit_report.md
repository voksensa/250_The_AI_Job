# Codebase Violation Audit Report

**Date**: 2025-11-21  
**Auditor**: Developer  
**Reviewed By**: CEO (pending)  

---

## Executive Summary

- **Total files audited**: ~20 (Core constitution, manuals, and available source code)
- **Total violations found**: 9 (including CEO's initial findings)
- **Critical violations (blocking)**: 5
- **Medium violations (should fix)**: 3
- **Low violations (cleanup)**: 1

**🚨 CRITICAL ALERT**: The codebase is currently in a **BROKEN STATE**. The `apps/agent-runtime` service cannot start because `routes.py` and `graph.py` are missing, despite being imported by `main.py`. This is a fundamental violation of "Production from Line 1".

---

## Critical Violations (MUST FIX)

### V-001: Broken Codebase (Missing Files)
- **File**: `apps/agent-runtime/src/agent_runtime/main.py:10`
- **Type**: Broken Code / Production from Line 1 Violation
- **Found**: `from .api.routes import router as tasks_router`
- **Violation**: The `api` directory and `routes.py` file do not exist in the codebase. `graph.py` is also missing. The service cannot run.
- **Evidence**: File system listing of `apps/agent-runtime/src/agent_runtime` shows only `__init__.py` and `main.py`.
- **Fix**: Restore or implement `api/routes.py` and `graph.py` immediately.

### V-002: "Dummy Build Pipeline" in Phase 0
- **File**: `constitution/ROADMAP_SPEC.md:202-203`
- **Type**: Mock/Placeholder Violation
- **Found**: 
  ```markdown
  * Executes a dummy build pipeline.
  * Produces a minimal app artifact.
  ```
- **Violation**: Contradicts "Production from Line 1". Even Phase 0 must build a real, deployable artifact, not a "dummy" one.
- **Evidence**: `AGENTS.md:26`: "No stubs, no mocks".
- **Fix**: Rewrite to specify a "production-grade starter app" with real dependencies.

### V-003: "Minimal Build Story"
- **File**: `constitution/ROADMAP_SPEC.md:243`
- **Type**: Mock/Placeholder Violation
- **Found**: "Inspect a minimal build story"
- **Violation**: "Minimal" implies incomplete. Build stories must be comprehensive from the start.
- **Fix**: Change to "Inspect a complete build story".

### V-004: Gate Requirement Contradiction
- **File**: `constitution/ROADMAP_SPEC.md:220` vs `CLAUDE.md:38`
- **Type**: Contradiction
- **Found**:
  - `ROADMAP_SPEC.md`: "Start with a minimal but strict subset of gates (G1–G5)"
  - `CLAUDE.md`: "Every deliverable must pass ALL gates (G1-G11)"
- **Violation**: Ambiguity on quality standards.
- **Fix**: Update `CLAUDE.md` to explicitly allow Phase 0/1 to target specific subsets (G1-G5), or update `ROADMAP_SPEC.md` to require all gates.

### V-005: "Minimal Testing" in Prototype Mode
- **File**: `constitution/STRATEGY.md:41`
- **Type**: Quality Violation
- **Found**: "**Prototype Mode**: Fast, cheap, minimal testing (2-5 minutes)"
- **Violation**: "Minimal testing" suggests skipping quality gates. Prototype mode should still pass core tests, just perhaps fewer scenarios.
- **Fix**: Clarify that "Prototype Mode" runs *essential* tests (lint, unit, smoke), not *minimal* ones.

---

## Medium Violations (SHOULD FIX)

### V-006: "Simple/Basic" Language
- **File**: `constitution/ROADMAP_SPEC.md` (multiple locations)
- **Type**: Generic/Vague Language
- **Found**: "simple funnel", "basic CRUD works"
- **Violation**: Vague terms allow for corner-cutting.
- **Fix**: Define concrete functional requirements (e.g., "CRUD with validation and error handling").

### V-007: "Minimal App Artifact"
- **File**: `constitution/ROADMAP_SPEC.md:203`
- **Type**: Mock/Placeholder Violation
- **Found**: "Produces a minimal app artifact"
- **Violation**: Similar to V-002, implies non-production quality.
- **Fix**: Change to "production-ready starter artifact".

### V-008: Missing LangGraph Verification
- **File**: `apps/agent-runtime`
- **Type**: Verification Failure
- **Found**: Unable to verify `PostgresSaver`, `astream`, or `get_stream_writer` usage because the code is missing.
- **Violation**: Cannot confirm adherence to "Native over Custom" principle.
- **Fix**: Once V-001 is fixed, immediate audit of `graph.py` is required.

---

## Low Violations (CLEANUP)

### V-009: "Minimal Documentation" Context
- **File**: `constitution/STATE_MANAGEMENT.md:766`
- **Type**: Contextual Clarification
- **Found**: "Only minimal docs; lean on code and chat."
- **Status**: **False Positive / Clarification**. This text describes a *rejected* option (`docs_sparse`).
- **Fix**: Ensure the table formatting makes it clear this is a rejected alternative, or rephrase to avoid confusion.

---

## LangGraph Native Verification

**Status**: 🔴 **FAILED / BLOCKED**

Unable to verify LangGraph patterns because the implementation files (`graph.py`, `routes.py`) are missing from the codebase.

**Required Checks (Pending Fix of V-001):**
1.  Verify `PostgresSaver` usage (not `MemorySaver`).
2.  Verify `astream` usage for event streaming.
3.  Verify `get_stream_writer` for custom events.
4.  Verify `langgraph-checkpoint-postgres` version.

---

## Contradictions Matrix

| File A | Line | Says | File B | Line | Says | Resolution |
|--------|------|------|--------|------|------|------------|
| `ROADMAP_SPEC.md` | 220 | "subset of gates (G1–G5)" | `CLAUDE.md` | 38 | "pass ALL gates (G1-G11)" | Update `CLAUDE.md` to reflect phased gate rollout. |
| `ROADMAP_SPEC.md` | 202 | "dummy build pipeline" | `AGENTS.md` | 26 | "No stubs, no mocks" | Update `ROADMAP_SPEC.md` to remove "dummy". |

---

## CEO Findings Validation

CEO provided 8 initial findings. Developer validation:
- **Confirmed**: 7 (V-CEO-001 to V-CEO-006, V-CEO-008)
- **False Positives**: 1 (V-CEO-007 - "Minimal Documentation" was describing a rejected option)
- **Additional Violations**: 1 (V-001 - The codebase is physically broken/missing files)

---

## Recommendations

### Immediate Actions (Critical)
1.  **Restore Missing Code**: Locate or rewrite `apps/agent-runtime/src/agent_runtime/api/routes.py` and `graph.py`. The system is currently non-functional.
2.  **Update Constitution**: Edit `ROADMAP_SPEC.md` and `STRATEGY.md` to remove "dummy", "mock", and "minimal" language. Replace with "production-grade", "starter", and "essential".
3.  **Align Gates**: Update `CLAUDE.md` to explicitly state which gates apply to Phase 0/1 (G1-G5) vs later phases.

### Systematic Fixes
1.  **CI Check for Forbidden Words**: Add a CI step to grep for "dummy", "mock", "stub" in documentation and code (excluding explicit negative examples).
2.  **Architecture Audit**: Once code is restored, perform the LangGraph native verification immediately.
