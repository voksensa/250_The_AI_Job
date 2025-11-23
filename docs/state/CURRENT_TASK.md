# CURRENT TASK

**Task ID**: TASK-P1-004-DEPLOYMENT-FIX  
**Title**: Sandbox Hosting Layer (Per-Task Port Allocation)  
**Phase**: Phase 1 – Production Toggle MVP  
**Owner**: Developer (awaiting invocation)  
**Status**: NOT STARTED  
**Created**: 2025-11-23  
**Target Gates**: G4 (Lint/Types), G5 (Tests/Coverage), G6 (Builds)  
**DEV_MODEL**: GPT

---

## Objective

Build sandbox hosting layer with **per-task unique port allocation** so generated files in `/workspace/{task_id}/` are accessible at `http://localhost:{port}` for Owner/QA validation.

## Definition of Done

- [ ] Each task allocated unique port (3100-3199 range)
- [ ] Files served via HTTP at `http://localhost:{port}/`
- [ ] RFC 9457 error responses
- [ ] ≥85% test coverage
- [ ] Full evidence (G4/G5/G6 artifacts, Docker logs, browser + DevTools screenshots)

## Next Action

**Owner**: Invoke Developer with `TASK-P1-004-DEPLOYMENT-FIX.md` to test hardened pipeline.
