# TASK-P1-003-DEPLOYMENT

## Metadata

- **Task ID**: TASK-P1-003-DEPLOYMENT
- **Phase**: Phase 1 – Production Toggle MVP
- **Owner**: Developer (awaiting invocation)
- **Status**: REJECTED – awaiting remediation per `VALIDATION_TASK-P1-003-DEPLOYMENT.md`
- **Created**: 2025-11-23
- **Blocks**: Phase 1 exit, Owner validation, Synthetic QA
- **Target Gates**: G6 (Builds), G5 (Tests)

## Problem Statement

Files generated in `/workspace/{task_id}/` exist but aren't served as live web apps. Synthetic QA fails (80%) trying to test `file://` URLs instead of `http://` deployed apps.

## Objective

Build sandbox hosting layer: files in `/workspace/{task_id}/` become accessible as live `http://localhost:{port}` web apps that Owner can validate in browser.

## Constraints

- Docker-only (no local dev server)
- Production from Line 1 (real HTTP server, not stubs)
- Must support multiple task IDs simultaneously (unique ports)
- ≥85% test coverage

## Acceptance Criteria

- [ ] Generated files (HTML/JS/CSS) served via HTTP on unique port per task
- [ ] Owner can visit `http://localhost:{port}` and interact with generated app
- [ ] Synthetic QA can navigate to deployed URLs successfully
- [ ] Docker proof: screenshot of browser showing deployed app
- [ ] ≥85% test coverage on hosting service
- [ ] Evidence captured in `evidence/G6/`

## Plan

1. Create `apps/sandbox-host/` service (FastAPI or simple HTTP server)
2. Mount `/workspace/` volumes from agent-runtime
3. Serve files at `http://localhost:{port}/{task_id}/index.html`
4. Add port allocation logic (starting at 3000, increment per task)
5. Update `docker-compose.yml` to expose ports
6. Test end-to-end: task creation → file generation → deployment → browser validation
7. Capture Docker proof (build logs, `docker ps`, browser screenshot)

## Next Action

- Developer to re-open task, implement per-task port allocation + Problem Details errors per spec.
- Regenerate ≥85% coverage + Docker/browser evidence for sandbox hosting.
- Resubmit for validation referencing `VALIDATION_TASK-P1-003-DEPLOYMENT.md` remediation list.
