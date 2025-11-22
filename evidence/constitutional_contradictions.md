# Constitutional Contradictions

## Contradiction #1: Test Coverage Thresholds
- **File A (`GOLDEN_RULES.md`) says**: "All NEW or CHANGED code must have ≥ **85% line coverage**." (Rule 1)
- **File B (`NOVEMBER_2025_STANDARDS.md`) says**: "New/changed backend code: ≥80%... New/changed frontend logic: ≥70%... Overall project: ≥60%".
- **File C (`ROADMAP_SPEC.md`) says**: "≥80% line coverage on new or modified backend code; ≥70% on new frontend logic".
- **Recommendation**: **Keep A (`GOLDEN_RULES.md`)**. It is the most recent (2025-11-22) and explicitly states it is "Adopted From: RB-003 (Tier 1 Immediate Enforcement)" and "If conflict: GOLDEN_RULES wins". `NOVEMBER_2025_STANDARDS.md` and `ROADMAP_SPEC.md` need to be updated to reflect the stricter 85% threshold.

## Contradiction #2: Next.js Version
- **File A (`STATE_MANAGEMENT.md`) says**: "[D-001] 2025-11-21 – Stack.frontend... Next.js 16 selected as frontend framework." (In DECISIONS LOG example/record).
- **File B (`OPERATIONAL_CONTEXT.md`) says**: "Framework: Next.js 15 (App Router)".
- **File C (`NOVEMBER_2025_STANDARDS.md`) says**: "Node 22 LTS... Next.js" (Version not explicitly pinned in text, but implies modern).
- **Recommendation**: **Clarify**. `STATE_MANAGEMENT.md` lists D-001 as an "Accepted" decision on 2025-11-21. `OPERATIONAL_CONTEXT.md` is dated 2025-11-20. If D-001 is a real decision, Next.js 16 is the standard. However, Next.js 16 might be a typo or a forward-looking statement if it's not stable yet (as of late 2025 context). Assuming "Next.js 16" is the intended decision if it exists, otherwise stick to 15. *Correction*: Next.js 15 is the current stable release in late 2024/early 2025. Next.js 16 would be bleeding edge. `OPERATIONAL_CONTEXT.md` is likely safer, but `STATE_MANAGEMENT.md` explicitly logs it as a decision. **Action**: Verify if D-001 is a real decision or just an example in the spec. If real, update `OPERATIONAL_CONTEXT.md`. If example, ignore. Given `STATE_MANAGEMENT.md` is a *spec* for state management, the log might be illustrative. However, `OPERATIONAL_CONTEXT.md` is the "Navigation Guide". I will assume Next.js 15 is the safe default unless explicitly told otherwise, but I should flag this.

## Contradiction #3: Architecture Documentation
- **File A (`ENGINE_ARCHITECTURE_V1.md`)**: Defines the agent graph.
- **File B (`langgraph_mapping_depreciated.md`)**: Deprecated visual builder plan.
- **Recommendation**: **Archive B**. It is explicitly deprecated.

## Contradiction #4: Execution Protocols
- **File A (`EXECUTION_PROTOCOL_SPEC.md`)**: Detailed execution steps.
- **File B (`CLAUDE.md`)**: Referenced as "CEO quality gates".
- **Recommendation**: **Merge/Align**. `EXECUTION_PROTOCOL_SPEC.md` seems to be the detailed implementation of `CLAUDE.md`. `CLAUDE.md` should probably remain as the high-level "Constitution" (as per `OPERATIONAL_CONTEXT.md`), but `EXECUTION_PROTOCOL_SPEC.md` is the "How-To". Ensure they don't conflict. (Did not read `CLAUDE.md` in this task, but it's a known constitutional file).

## Contradiction #5: Tech Stack Details
- **File A (`ARCHITECTURAL_DECISIONS.md`)**: "Put `/api/v1/` on every backend URL".
- **File B (`OPERATIONAL_CONTEXT.md`)**: Does not explicitly mention API versioning in the summary.
- **Recommendation**: **Update B**. `OPERATIONAL_CONTEXT.md` should reflect the `/api/v1/` decision to avoid confusion.

## Contradiction #6: Tailwind Version
- **File A (`STATE_MANAGEMENT.md`)**: "[D-002]... Tailwind 4 selected".
- **File B (`OPERATIONAL_CONTEXT.md`)**: "Tailwind CSS".
- **Recommendation**: **Update B** to specify Tailwind 4 if that decision is active.
