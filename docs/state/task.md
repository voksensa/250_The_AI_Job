# CURRENT TASK

- Task ID: TASK-P1-002-FIX_executor-must-generate-files
- Title: Fix Executor Must Generate Real Files
- Owner: Developer
- Status: In Progress
- Related Phase: Phase 1 – MVP
- Target Gates: G1, G4, G5, G10
- Linked Specs:
  - TASK-P1-002-FIX_executor-must-generate-files.md

## Objective

Ensure the executor node generates actual files in a workspace volume instead of just text explanations, and allow these files to be downloaded via the API and viewed in the Owner Console.

## Definition of Done

- [ ] Executor node uses `create_file` tool.
- [ ] Workspace volume is mounted in Docker.
- [ ] Artifact download endpoint is implemented.
- [ ] Frontend displays file tree and download button.
- [ ] Unit tests pass with >85% coverage.
- [ ] Docker verification shows real files.

## Next Action (Mandatory)

Implement Phase A: Backend changes (executor node, volume, API).
