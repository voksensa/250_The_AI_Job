# TASK-FIX-002: Remediate Constitution Violations

**Assigned To**: Developer
**Created By**: CEO
**Priority**: 🔴 **CRITICAL / BLOCKING**
**Date**: 2025-11-21
**Blocks**: Phase 1 MVP (TASK-003)

## Objective
Fix all constitution violations identified in the codebase audit to ensure documentation is consistent with "Production from Line 1," "Native over Custom," and evidence-based principles.

## Violations to Fix
- [ ] **V-002**: "Dummy Build Pipeline" in `ROADMAP_SPEC.md`
- [ ] **V-003**: "Minimal Build Story" in `ROADMAP_SPEC.md`
- [ ] **V-004**: Gate Requirement Contradiction (`ROADMAP_SPEC.md` vs `CLAUDE.md`)
- [ ] **V-005**: "Minimal Testing" in `STRATEGY.md`
- [ ] **V-006**: Vague "Simple/Basic" Language in `ROADMAP_SPEC.md`
- [ ] **V-007**: "Minimal App Artifact" in `ROADMAP_SPEC.md`

## Implementation Steps
1. [ ] Create branch `fix/constitution-violations`
2. [ ] Fix V-002 & V-007 in `ROADMAP_SPEC.md`
3. [ ] Fix V-003 in `ROADMAP_SPEC.md`
4. [ ] Fix V-004 (Option A: Phased rollout) in `CLAUDE.md` and `ROADMAP_SPEC.md`
5. [ ] Fix V-005 in `STRATEGY.md`
6. [ ] Fix V-006 (Search and replace "simple", "basic") in `ROADMAP_SPEC.md`
7. [ ] Search for additional forbidden words ("dummy", "minimal", "mock", "stub")
8. [ ] Verify fixes and consistency
9. [ ] Create Session Log
10. [ ] Update `BLOCKERS.md` and `PROGRESS.md`

## Verification
- [ ] Grep for forbidden words returns zero results (except negative examples)
- [ ] ROADMAP and CLAUDE agree on gates
- [ ] Git diff shows only constitution changes

## References
- `audit_report.md`
- `constitution/ROADMAP_SPEC.md`
- `constitution/STRATEGY.md`
- `constitution/CLAUDE.md`
