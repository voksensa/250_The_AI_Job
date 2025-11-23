# TASK-P1-004-DEPLOYMENT-FIX

## Metadata

- **Task ID**: TASK-P1-004-DEPLOYMENT-FIX
- **Phase**: Phase 1 – Production Toggle MVP
- **Owner**: Developer (awaiting invocation)
- **Status**: Not Started
- **Created**: 2025-11-23
- **Supersedes**: TASK-P1-003-DEPLOYMENT (failed validation)
- **Blocks**: Phase 1 exit, Owner validation, Synthetic QA
- **Target Gates**: G4 (Lint/Types), G5 (Tests/Coverage), G6 (Builds)
- **DEV_MODEL**: GPT (testing hardened pipeline with GPT-5.1-Codex)

## Problem Statement

Files generated in `/workspace/{task_id}/` exist but aren't served as live web apps accessible at unique `http://localhost:{port}` URLs. Synthetic QA fails (80%) because it cannot navigate to deployed apps.

## Objective

Build sandbox hosting layer that serves generated files from `/workspace/{task_id}/` as live web apps, **with each task allocated a unique port** such that Owner/QA can access them at `http://localhost:{port}`.

## Constraints

- **Docker-only** (no local dev server)
- **Production from Line 1** (real HTTP server, not stubs)
- **Per-task unique ports** (e.g., task A → 3100, task B → 3101)
- **RFC 9457 Problem Details** for all error responses
- **≥85% test coverage** on new code
- **Full evidence** (coverage report, Docker logs, browser screenshot, DevTools screenshot)

## Acceptance Criteria

### AC1: Per-Task Port Allocation
- [ ] Each task gets a unique port in range 3100-3199
- [ ] Port allocation tracked (e.g., in DB or simple registry)
- [ ] Owner can access task at `http://localhost:{allocated_port}/`
- [ ] Multiple tasks can run simultaneously on different ports

### AC2: File Serving
- [ ] Files in `/workspace/{task_id}/` served as static files
- [ ] Default to `index.html` if path is `/`
- [ ] Proper MIME types for HTML/CSS/JS

### AC3: RFC 9457 Compliance
- [ ] All 4xx/5xx errors use `ProblemDetail` schema with fields: `type`, `title`, `status`, `detail`, `instance`
- [ ] No bare `{"detail": "..."}` responses

### AC4: Docker Proof (G6)
- [ ] `docker-compose build` output captured to `evidence/G6/TASK-P1-004-build.log`
- [ ] `docker ps` output showing service running captured to `evidence/G6/TASK-P1-004-docker-ps.txt`
- [ ] `curl` output against deployed task captured to `evidence/G6/TASK-P1-004-curl.txt`
- [ ] Browser screenshot of working app saved to `evidence/G6/TASK-P1-004-browser.png`
- [ ] DevTools console screenshot (zero errors) saved to `evidence/G6/TASK-P1-004-devtools.png`

### AC5: Testing & Coverage (G5)
- [ ] Unit tests for port allocation logic
- [ ] Unit tests for file serving
- [ ] Integration test: create task → allocate port → serve file → verify access
- [ ] ≥85% coverage on new `sandbox-proxy` code
- [ ] Coverage report saved to `evidence/G5/TASK-P1-004-coverage.txt` and `evidence/G5/TASK-P1-004-coverage.html`
- [ ] Pytest output saved to `evidence/G5/TASK-P1-004-pytest.txt`

### AC6: Code Quality (G4)
- [ ] Lint clean (ruff)
- [ ] Type check clean (mypy)
- [ ] Output saved to `evidence/G4/TASK-P1-004-lint.txt` and `evidence/G4/TASK-P1-004-types.txt`

## Implementation Notes

**Port Allocation Strategy**: Use a simple in-memory registry (start at 3100, increment). Persist in Postgres if time allows, otherwise document as Phase 2 improvement.

**Docker Compose**: Add service definition for `sandbox-proxy` with port range 3100-3199 exposed.

**RFC 9457 Schema**: Create `ProblemDetail` Pydantic model and FastAPI exception handler.

## Evidence Requirements Summary

All evidence files MUST exist before Validator review:

**G4 (Code Quality)**:
- `evidence/G4/TASK-P1-004-lint.txt`
- `evidence/G4/TASK-P1-004-types.txt`

**G5 (Tests/Coverage)**:
- `evidence/G5/TASK-P1-004-pytest.txt`
- `evidence/G5/TASK-P1-004-coverage.txt`
- `evidence/G5/TASK-P1-004-coverage.html/` (directory)

**G6 (Builds/Docker)**:
- `evidence/G6/TASK-P1-004-build.log`
- `evidence/G6/TASK-P1-004-docker-ps.txt`
- `evidence/G6/TASK-P1-004-curl.txt`
- `evidence/G6/TASK-P1-004-browser.png`
- `evidence/G6/TASK-P1-004-devtools.png`

## Next Action

Awaiting Owner to invoke Developer with this task spec.
