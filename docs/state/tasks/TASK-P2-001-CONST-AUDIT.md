# TASK-P2-001-CONST-AUDIT: Constitutional Files Audit

**Priority**: 🔴 **HIGH** (Blocks Phase 2 expansion)  
**Order**: Task 1 of 4 (Phase 2 Foundation)  
**Estimated**: 4-6 hours

---

## Objective

Audit all 12 constitutional files for contradictions, redundancy, and outdated content. Create merge/archive plan before Phase 2 expansion.

---

## Current State

**Constitutional Files** (12 total):
1. `ARCHITECTURAL_DECISIONS.md` (8KB)
2. `ENGINE_ARCHITECTURE_V1.md` (5.8KB)
3. `EXECUTION_PROTOCOL_SPEC.md` (10.8KB)
4. `NOVEMBER_2025_STANDARDS.md` (15KB)
5. `OPERATIONAL_CONTEXT.md` (7.7KB)
6. `ROADMAP_SPEC.md` (25.8KB)
7. `STATE_MANAGEMENT.md` (35KB)
8. `STRATEGY.md` (8.4KB)
9. `VISION.md` (7.7KB)
10. `langgraph_mapping_depreciated.md` (22.6KB) ⚠️ **DEPRECATED**
11. `session_summary.md` (4.9KB)
12. `GOLDEN_RULES.md` (NEW - 2025-11-22)

**Total**: ~155KB

---

## Tasks

### Phase A: Read & Categorize (2hr)

**For each file**:
1. Read completely
2. Extract key rules/decisions
3. Note primary domain
4. Identify overlaps with other files
5. Check last update date

**Output**: `evidence/constitutional_audit_matrix.md`

**Format**:
| File | Domain | Key Content | Overlaps | Status | Last Updated |
|------|--------|-------------|----------|--------|--------------|

---

### Phase B: Identify Contradictions (1hr)

**Look for**:
- Conflicting quality gate thresholds
- Different architecture patterns
- Outdated tech specs
- Rules that conflict with GOLDEN_RULES.md
- Different execution protocols

**Output**: `evidence/constitutional_contradictions.md`

**Format**:
- **Contradiction #N**: [description]
  - File A says: [X]
  - File B says: [Y]
  - Recommendation: [keep A / keep B / new rule]

---

### Phase C: Create Merge/Archive Plan (2hr)

**Propose**:

1. **ARCHIVE** (→ `constitution/archive/`):
   - `langgraph_mapping_depreciated.md` (already deprecated)
   - Any other truly outdated files

2. **MERGE** (consolidate redundant):
   - Example: Multiple architecture docs → one canonical
   - Example: Multiple execution specs → one protocol

3. **PRESERVE** (keep as-is):
   - Files with unique, current value
   - GOLDEN_RULES.md
   - VISION.md

4. **UPDATE** (fix contradictions):
   - Files needing alignment

**Output**: `docs/state/CONST_MERGE_PLAN.md`

---

### Phase D: Get Approval (30min)

Submit plan to CEO → Owner before executing.

---

## Success Criteria

✅ **Matrix Complete**: All 12 files categorized  
✅ **Contradictions** Documented  
✅ **Merge Plan**: Clear, justified  
✅ **No Content Loss**: Everything archived, not deleted  
✅ **Owner Approval**: Before execution

---

## Next Task After Approval

If plan approved:
- **TASK-P2-001-EXECUTE**: Implement merge/archive (2-3hr)
- Then proceed to TASK-P2-002-OPENAPI

**This task blocks Phase 2 expansion**
