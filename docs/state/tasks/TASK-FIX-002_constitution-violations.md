# TASK-FIX-002: Remediate Constitution Violations

**Assigned To**: Developer  
**Created By**: CEO  
**Priority**: 🔴 **CRITICAL / BLOCKING**  
**Date**: 2025-11-21  
**Blocks**: Phase 1 MVP (TASK-003) - Cannot build on inconsistent foundation  
**Estimated Effort**: 1-2 hours  
**Audit Reference**: `audit_report.md` violations V-002 through V-007

---

## Objective

Fix all constitution violations identified in the codebase audit to ensure documentation is consistent with "Production from Line 1," "Native over Custom," and evidence-based principles.

**Non-Negotiable Requirements:**
1. **Line-Level Precision** - Every fix must cite exact line numbers
2. **Evidence-Based** - Changes must align with CLAUDE.md, AGENTS.md, VISION.md
3. **No Exceptions** - All violations must be addressed, no partial fixes
4. **Verification** - CEO will grep for forbidden words after submission

---

## Context

**Audit Findings Summary:**
- ✅ V-001: Broken codebase - RESOLVED in TASK-FIX-001
- ❌ V-002 to V-007: Constitution contains language that violates core principles
- 🚨 **Impact**: Cannot proceed to Phase 1 with contradictory documentation

**Why This Matters:**
- Constitution guides all development decisions
- Contradictions cause developer confusion and wrong implementations
- "Dummy," "minimal," "mock" language normalizes violations
- Quality gate ambiguity creates escape hatches

---

## Violations to Fix

### V-002: "Dummy Build Pipeline" (CRITICAL)

**File**: `constitution/ROADMAP_SPEC.md`  
**Lines**: 202-203  

**Current (WRONG):**
```markdown
* Executes a dummy build pipeline.
* Produces a minimal app artifact.
```

**Violation**: Contradicts "Production from Line 1" (AGENTS.md:26: "No stubs, no mocks")

**Required Fix:**
```markdown
* Executes a production-grade build pipeline with real dependencies.
* Produces a deployable starter app artifact.
```

**Verification**: Grep for "dummy" in ROADMAP_SPEC.md must return zero results (excluding this as a negative example).

---

### V-003: "Minimal Build Story" (CRITICAL)

**File**: `constitution/ROADMAP_SPEC.md`  
**Line**: 243  

**Current (WRONG):**
```markdown
* Inspect a minimal build story (what was built, which tests ran).
```

**Violation**: "Minimal" implies incomplete. Build stories must be comprehensive from Line 1.

**Required Fix:**
```markdown
* Inspect a complete build story showing what was built, which tests ran, and all quality gates checked.
```

**Verification**: Search for "minimal build story" must return zero results.

---

### V-004: Gate Requirement Contradiction (CRITICAL)

**Files**: `constitution/ROADMAP_SPEC.md:220` vs `CLAUDE.md:38`  

**Current Contradiction:**
- ROADMAP_SPEC.md line 220: "Start with a minimal but strict subset of gates (G1–G5)"
- CLAUDE.md line 38: "Every deliverable must pass ALL gates (G1-G11)"

**Violation**: Creates ambiguity on which gates apply when.

**Required Fix (Option A - Recommended):**

Update `CLAUDE.md` line 38 to add phased rollout clarity:
```markdown
**G0 - Gate Applicability**
- Phase 0: Gates G1-G5 (Research, Architecture, Lint, Evidence, Type Safety)
- Phase 1: Gates G1-G7 (adds G6: Builds, G7: Basic Tests)
- Phase 2+: ALL gates G1-G11

Every deliverable must pass ALL gates applicable to its phase.
```

Update `ROADMAP_SPEC.md` line 220 to reference this:
```markdown
**Mitigation:** Use phased gate rollout per CLAUDE.md G0 (G1–G5 in P0, expanding in later phases).
```

**OR Option B (Stricter):**

Remove the exception from ROADMAP_SPEC.md line 220:
```markdown
**Mitigation:** Enforce strict gate compliance (G1-G11) from Phase 0. Budget additional time for quality verification.
```

**Your Choice**: Pick Option A or B, document reasoning in session log citing CLAUDE.md and ROADMAP_SPEC.md context.

**Verification**: No contradictions between ROADMAP and CLAUDE on gate requirements.

---

### V-005: "Minimal Testing" in Prototype Mode (CRITICAL)

**File**: `constitution/STRATEGY.md`  
**Line**: 41  

**Current (WRONG):**
```markdown
- **Prototype Mode**: Fast, cheap, minimal testing (2-5 minutes)
```

**Violation**: "Minimal testing" suggests skipping quality gates. Even prototypes must meet quality standards.

**Required Fix:**
```markdown
- **Prototype Mode**: Fast, essential testing (lint, unit tests, smoke tests) (2-5 minutes)
```

**Verification**: Search for "minimal testing" must return zero results.

---

### V-006: Vague "Simple/Basic" Language (MEDIUM)

**File**: `constitution/ROADMAP_SPEC.md`  
**Multiple Locations** (you must find all instances)

**Examples Found in Audit:**
- "simple funnel"
- "basic CRUD works"

**Violation**: Vague terms allow corner-cutting. Requirements must be concrete.

**Required Fix Pattern:**
- "simple funnel" → "user registration and task submission funnel with validation"
- "basic CRUD works" → "CRUD with input validation, error handling, and persistence"

**Steps:**
1. Grep for "simple ", "basic ", "trivial " in ROADMAP_SPEC.md
2. For each instance, replace with concrete functional requirement
3. Document all replacements in session log with line numbers

**Verification**: CEO will review each replacement for concreteness.

---

### V-007: "Minimal App Artifact" (MEDIUM)

**File**: `constitution/ROADMAP_SPEC.md`  
**Line**: 203  

**Current (WRONG):**
```markdown
* Produces a minimal app artifact.
```

**Violation**: Same as V-002 - implies non-production quality.

**Required Fix:**
```markdown
* Produces a production-ready starter app artifact.
```

**Note**: This is part of the same section as V-002. Ensure both lines are fixed together.

**Verification**: Grep for "minimal app" must return zero results.

---

## Implementation Steps

### Step 1: Create Working Branch

```bash
cd /Users/Yousef_1/Downloads/250_The_AI_Job
git checkout -b fix/constitution-violations
```

### Step 2: Fix Each Violation

For each violation V-002 through V-007:

1. Open the file
2. Locate the exact line(s)
3. Apply the required fix
4. Document in session log:
   - Violation ID
   - File and line numbers
   - Old text (quoted)
   - New text (quoted)
   - Rationale citing CLAUDE.md or AGENTS.md

### Step 3: Search for Additional Instances

**Required Searches:**

```bash
# Search for forbidden words in constitution files
cd constitution/
grep -n "dummy" *.md
grep -n "minimal" *.md
grep -n "mock" *.md
grep -n "stub" *.md
grep -n "simple " *.md
grep -n "basic " *.md
grep -n "trivial" *.md
```

**For each result:**
- Evaluate if it's a violation or acceptable usage (e.g., in a negative example)
- If violation: Fix it and document
- If acceptable: Document why it's acceptable in session log

### Step 4: Verify Gate Alignment

**Check these files for gate requirement consistency:**
- `CLAUDE.md` - What gates are required?
- `constitution/ROADMAP_SPEC.md` - What gates does it mention?
- `constitution/STRATEGY.md` - Any gate references?

**Ensure**: All files agree on gate requirements per phase.

---

## Verification Requirements

### V1: Forbidden Words Check

```bash
cd constitution/
grep -i "dummy\|minimal\|mock\|stub" *.md | grep -v "# Examples of BAD" | grep -v "rejected option"
```

**Expected**: No results (or only results in explicit negative examples with clear "BAD" markers)

### V2: Line-by-Line Verification

For each fixed violation, CEO will:
1. Open the file
2. Check the exact line number
3. Verify text matches required fix
4. Confirm no forbidden words remain

### V3: Consistency Check

```bash
# Verify ROADMAP and CLAUDE agree on gates
grep -n "gates" constitution/ROADMAP_SPEC.md constitution/CLAUDE.md
```

**Expected**: No contradictions on which gates apply when.

### V4: Git Diff Review

```bash
git diff main..fix/constitution-violations
```

**Expected**: Only constitution files modified, all changes explained in session log.

---

## Documentation Requirements

### D1: Session Log

Create: `docs/state/SESSIONS/2025-11-21_dev_fix002-constitution.md`

**Structure:**

```markdown
# Session Log: Constitution Violation Remediation (TASK-FIX-002)

## Violations Fixed

### V-002: Dummy Build Pipeline
- **File**: constitution/ROADMAP_SPEC.md
- **Lines**: 202-203
- **Old Text**: [paste original]
- **New Text**: [paste replacement]
- **Rationale**: Violates AGENTS.md:26 "No stubs, no mocks". Changed to "production-grade" per audit requirement.

[Repeat for V-003 through V-007]

## Additional Findings

### Search Results: "simple" in ROADMAP_SPEC.md
- Line 85: "simple funnel" → Fixed to "registration and task submission funnel with validation"
- Line 142: "simple interface" → Acceptable (describes UX principle, not quality)

[Document all search results and decisions]

## Gate Alignment Decision

### V-004 Resolution
- **Chose**: Option A (Phased gate rollout)
- **Rationale**: [cite ROADMAP context, explain why phased makes sense]
- **Changes**: 
  - Added G0 to CLAUDE.md at line [X]
  - Updated ROADMAP_SPEC.md line 220 to reference G0

## Verification Results

### Forbidden Words Check
[paste command output]
Result: ✅ PASS - No forbidden words outside negative examples

### Git Diff Summary
[paste git diff --stat]
Files changed: 3
Lines modified: ~15

## Conclusion
All constitution violations (V-002 through V-007) resolved. Documentation is now consistent with "Production from Line 1" and evidence-based principles.
```

---

### D2: Update BLOCKERS.md

Mark violations as resolved:

```markdown
## Resolved

- **ID**: V-002, V-003, V-004, V-005, V-006, V-007
  - **Date**: 2025-11-21
  - **Resolution**: Constitution language fixed to remove "dummy", "minimal", "mock", and vague terms
  - **Task**: TASK-FIX-002
  - **Evidence**: Session log SESSIONS/2025-11-21_dev_fix002-constitution.md
```

---

### D3: Update PROGRESS.md

```markdown
- **2025-11-21** – Developer – Completed TASK-FIX-002: Fixed constitution violations (V-002 to V-007). Removed "dummy", "minimal", "mock" language. Aligned gate requirements across ROADMAP and CLAUDE.
```

---

## Success Criteria

You are DONE when:

- [ ] All 6 violations (V-002 through V-007) are fixed with exact line-level changes
- [ ] Grep for forbidden words returns zero violations
- [ ] ROADMAP_SPEC.md and CLAUDE.md agree on gate requirements
- [ ] V-004 resolution (Option A or B) is documented with rationale
- [ ] Session log documents every fix with before/after text
- [ ] Additional search results documented (all "simple", "basic", etc.)
- [ ] BLOCKERS.md updated
- [ ] PROGRESS.md updated
- [ ] All changes committed to git with detailed message
- [ ] Working branch merged to main

---

## Git Commit Message Template

```
fix(constitution): Remediate audit violations V-002 to V-007

CRITICAL fixes to align constitution with "Production from Line 1" principles.

Changes:
- ROADMAP_SPEC.md: Remove "dummy build pipeline" → "production-grade pipeline"
- ROADMAP_SPEC.md: Remove "minimal build story" → "complete build story"
- ROADMAP_SPEC.md: Remove "minimal app artifact" → "production-ready artifact"
- STRATEGY.md: Remove "minimal testing" → "essential testing"
- ROADMAP_SPEC.md + CLAUDE.md: Align gate requirements (phased rollout)
- ROADMAP_SPEC.md: Replace vague "simple/basic" with concrete requirements

All forbidden words ("dummy", "minimal", "mock", "stub") removed from constitution.
Gate contradiction (V-004) resolved with [Option A/B].

Evidence: docs/state/SESSIONS/2025-11-21_dev_fix002-constitution.md
Audit: audit_report.md violations V-002 through V-007
```

---

## CEO Review Checklist

When you submit, I will verify:

- [ ] Every violation V-002 to V-007 fixed at exact line numbers
- [ ] No "dummy", "minimal", "mock", "stub" in constitution files (except negative examples)
- [ ] ROADMAP and CLAUDE agree on gates
- [ ] V-004 resolution documented with clear rationale
- [ ] Session log has before/after text for every fix
- [ ] All grep search results documented
- [ ] Git commit message follows template
- [ ] Working branch clean (only constitution files modified)

**If any item fails, task will be REJECTED and returned to you.**

---

## Critical Reminders

1. **PRECISION REQUIRED**
   - Fix exact lines cited in violations
   - Quote original text in session log
   - Quote replacement text in session log

2. **NO PARTIAL FIXES**
   - All 6 violations must be addressed
   - Cannot skip "medium" violations
   - Must search for additional instances

3. **EVIDENCE REQUIRED**
   - Session log must show grep command outputs
   - Must document search results for "simple", "basic", etc.
   - Must show git diff before committing

4. **GATE DECISION**
   - V-004 requires you to choose Option A or B
   - Must document reasoning citing ROADMAP context
   - Must update both CLAUDE.md AND ROADMAP_SPEC.md

---

## Timeline

**Start**: Immediately  
**Expected Duration**: 1-2 hours focused work  
**Deadline**: End of work session (notify CEO when complete)

---

## Questions?

If you find additional violations during your searches:
1. Document them in session log under "Additional Findings"
2. Fix them using same pattern (concrete requirement vs vague term)
3. Include in your submission

If you're uncertain whether a word usage is a violation:
1. Ask yourself: "Does this normalize placeholder/mock/incomplete code?"
2. If yes: It's a violation, fix it
3. If no (e.g., "simple UX" as a design goal): Document as acceptable with reasoning

**Do NOT guess. Do NOT skip violations. EVERY instance must be addressed.**
