# Constitutional Merge/Archive Plan

**Status**: Draft
**Date**: 2025-11-22

## 1. Archive (Move to `constitution/archive/`)
These files are deprecated or historical context only.

- **`langgraph_mapping_depreciated.md`**
  - *Reason*: Explicitly deprecated and replaced by `ENGINE_ARCHITECTURE_V1.md`.
- **`session_summary.md`**
  - *Reason*: Historical context of the "Steve Jobs" pivot. Valuable for history but not active constitution.

## 2. Merge (Consolidate)
No full file merges required at this stage, but logical consolidation of rules is needed via updates.

## 3. Update (Resolve Contradictions)
These files remain active but need specific updates to align with `GOLDEN_RULES.md` and `ARCHITECTURAL_DECISIONS.md`.

- **`NOVEMBER_2025_STANDARDS.md`**
  - *Action*: Update coverage thresholds to **85%** (Backend/Frontend) to match `GOLDEN_RULES.md`.
  - *Action*: Explicitly reference `GOLDEN_RULES.md` as the overriding authority.
- **`ROADMAP_SPEC.md`**
  - *Action*: Update coverage success criteria to **85%**.
- **`OPERATIONAL_CONTEXT.md`**
  - *Action*: Update Tech Stack section to reflect:
    - **Next.js 16** (Owner confirmed)
    - **Tailwind CSS 4** (Owner confirmed)
    - **API v1** (`/api/v1/` pattern from `ARCHITECTURAL_DECISIONS.md`)

## 4. Preserve (Keep As-Is)
These files are core, active, and unique.

- **`VISION.md`** (North Star)
- **`STRATEGY.md`** (Business/Product Strategy)
- **`GOLDEN_RULES.md`** (Tier 1 Non-Negotiables)
- **`ARCHITECTURAL_DECISIONS.md`** (Architecture Rules)
- **`ENGINE_ARCHITECTURE_V1.md`** (Agent Graph Spec)
- **`EXECUTION_PROTOCOL_SPEC.md`** (Process Spec)
- **`STATE_MANAGEMENT.md`** (State Spec)

## Execution Steps (Next Task)
1. Create `constitution/archive/` directory.
2. Move `langgraph_mapping_depreciated.md` and `session_summary.md` to archive.
3. Edit `NOVEMBER_2025_STANDARDS.md` to bump coverage to 85%.
4. Edit `ROADMAP_SPEC.md` to bump coverage to 85%.
5. Edit `OPERATIONAL_CONTEXT.md` to add Next.js 16, Tailwind 4, and API v1 notes.
