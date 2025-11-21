# CURRENT TASK

- **Task ID**: TASK-003_production-toggle-mvp
- **Title**: Production Toggle MVP - End-to-End Workflow
- **Owner**: Developer
- **Status**: Ready to Start
- **Related Phase**: Phase 1 – MVP (Production Toggle Proof)
- **Target Gates**: G5 (Tests), G6 (Builds), G10 (Owner can use it)
- **Linked Specs**:
  - [COMPLETE_ARCHITECTURE_SPEC.md](../research/COMPLETE_ARCHITECTURE_SPEC.md)
  - [VISION.md](../../VISION.md)

## Objective

Build the first end-to-end Production Toggle feature: a simple task submission workflow with both backend (LangGraph) and frontend (Owner Console UI) working together.

## Definition of Done

- [ ] Backend: LangGraph workflow with 3 nodes (planner, coder, responder)
- [ ] Backend: FastAPI endpoints (`POST /api/tasks`, `GET /api/tasks/{id}`)
- [ ] Frontend: Task submission form on homepage
- [ ] Owner can submit task via UI and see response
- [ ] Tests passing, services healthy
- [ ] Committed to Git with session log

## Next Action (Mandatory)

**Developer**: Execute TASK-003 per task file. Implement Phase A (backend) and Phase B (frontend) together.

## CEO Needs To Decide (Optional)

None - Owner approved "Phase A + Phase B together" approach.

## Notes

Full task details: [docs/state/tasks/TASK-003_production-toggle-mvp.md](./tasks/TASK-003_production-toggle-mvp.md)
