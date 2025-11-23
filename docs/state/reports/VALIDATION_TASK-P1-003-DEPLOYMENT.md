# Validation Report — TASK-P1-003-DEPLOYMENT (Sandbox Hosting Layer)

**Validator**: Codex Validator – 2025-11-23T00:00Z  
**Date**: 2025-11-23  
**Verdict**: REJECTED

---

## 1. Summary

- **Task**: TASK-P1-003-DEPLOYMENT — Sandbox Hosting Layer
- **Phase**: Phase 1 – Production Toggle MVP
- **Gates in Scope**: G6 (Builds), G5 (Tests)
- **Diamond Risk**: PRESENT
- **Verdict**: REJECTED

---

## 2. What I Checked

- Task spec: `docs/state/tasks/TASK-P1-003-DEPLOYMENT.md`
- Evidence: `evidence/G6/TASK-P1-003-DEPLOYMENT-verification.md`, `evidence/G5/test_coverage*.txt`
- State spine: `docs/state/INDEX.md`, `CURRENT_TASK.md`, `PROGRESS.md`, `BLOCKERS.md`
- Implementation: `apps/sandbox-proxy/src/sandbox_proxy/*.py`, docker-compose service wiring

---

## 3. Findings

### 3.1 Golden Rules Check

- [x] Rule 0 (Diamond Rule): FAIL — Acceptance criteria requiring per-task ports were not met, and no waiver/owner decision was recorded (`docs/state/tasks/TASK-P1-003-DEPLOYMENT.md:25-35`).
- [x] Rule 0.1 (Diamond Analogy): FAIL — Shipping a shared-port proxy without documenting the risk burns future multi-app validation time; no Option A/B logged.
- [x] Rule 1 (Coverage ≥85%): FAIL — Only G5 artifacts available (`evidence/G5/test_coverage.txt` line 49, `test_coverage_remediation.txt` line 49) show overall coverage at 34–44%, and there is no coverage report for the new sandbox-proxy service.
- [x] Rule 2 (Production from line 1): PASS — Service is containerized in docker-compose with real FastAPI/uvicorn runtime.
- [x] Rule 3 (No big-bang refactors): PASS — Change isolated to new service + compose entry.
- [x] Rule 4 (Modular monolith boundaries): PASS — New code placed under `apps/sandbox-proxy/src/` per layout.

### 3.2 Architectural Decisions Check

- [x] D1 (API v1 endpoints): PASS — Management endpoints use `/api/v1/health`; static file route intentionally sits at root for user apps.
- [x] D2 (RFC 9457 errors): FAIL — `apps/sandbox-proxy/src/sandbox_proxy/main.py:33-87` raises bare `HTTPException` objects that emit FastAPI's `{"detail": ...}` payload instead of the mandated Problem Details schema.
- [x] D3 (Additive LangGraph state): PASS — No state schema changes.
- [x] D4 (src/ layout): PASS — Service follows `src/sandbox_proxy/...` layout.
- [x] D5 (snake_case): PASS — Settings and responses use snake_case.
- [x] D6 (Absolute imports): PASS — Module imports are absolute.

### 3.3 Gates Check

- **G6 (Builds)**: FAIL — Acceptance requires "unique port per task" and Docker/browser proof with screenshots (`docs/state/tasks/TASK-P1-003-DEPLOYMENT.md:25-35`). Implementation hardcodes a single port (`apps/sandbox-proxy/src/sandbox_proxy/settings.py:5-13`, `docker-compose.yml:41-52`), and evidence lacks the required Docker logs and screenshots (only narrative text in `evidence/G6/TASK-P1-003-DEPLOYMENT-verification.md`).
- **G5 (Testing & Coverage)**: FAIL — No artifact demonstrates sandbox-proxy tests or ≥85% coverage. The only coverage files present under G5 report 34% and 44% overall coverage for agent-runtime, contradicting the Golden Rule requirement and leaving new code unverified.

### 3.4 Docker Proof

- [x] Docker builds: FAIL — No build logs attached for sandbox-proxy.
- [x] Docker runs: FAIL — No `docker ps` / health-check output provided, only narrative statements.
- [x] Real UI screenshots: ABSENT — Requirement for a browser screenshot of the deployed sandbox app is unmet (`evidence/G6/` contains no images).
- [x] Real backend calls: NOT VERIFIED — No curl output or recorded responses beyond prose.

### 3.5 Diamond Risk Assessment

**Business Goal**: Allow Owner/Synthetic QA to browse real deployed task artifacts at `http://localhost:{port}` so Phase 1 Production Toggle can be validated end-to-end.

**Diamond Risk Analysis**: Current approach multiplexes every task through a single port without updating the spec or documenting an Option A/B choice. This undercuts the business goal (Owner still cannot reach `http://localhost:{port}` per task) and risks burning more validation cycles integrating QA against an unsupported pattern. Missing coverage evidence further risks shipping an unaudited network service.

**Safer Alternative**:
- **Option A (recommended)**: Honor the original acceptance criteria — allocate ports per task (e.g., via registry service), emit those URLs to the Owner UI/QA, and capture Docker/browser proof alongside ≥85% coverage artifacts.
- **Option B (current, risky)**: Share port 3001 for every task without agreeing on new semantics; no UI integration or proof, which blocks QA and wastes production time.

---

## 4. Required Remediation

1. Implement the specified per-task port allocation and expose those URLs (update `apps/sandbox-proxy/src/sandbox_proxy/settings.py:5-13`, router logic, and docker-compose) so each task is reachable at its own `http://localhost:{port}` (`docs/state/tasks/TASK-P1-003-DEPLOYMENT.md:25-35`).
2. Enforce RFC 9457 Problem Details in sandbox-proxy error responses (introduce a ProblemDetail schema and global exception handler in `apps/sandbox-proxy/src/sandbox_proxy/main.py:26-87`).
3. Produce G5 evidence for this task: run sandbox-proxy tests in Docker, capture the pytest + coverage output showing ≥85% for new code, and store it under `evidence/G5/TASK-P1-003-DEPLOYMENT_*` instead of the unrelated 34–44% logs.
4. Provide the mandated G6 proof artifacts: `docker-compose` build output, `docker ps` snapshot showing `yfe-sandbox-proxy`, curl output against real task URLs, and a browser screenshot demonstrating a served `/workspace/{task_id}/index.html` page.

---

## 5. Final Verdict

**REJECTED**: Multiple Golden Rule, Architectural Decision, and gate violations (per-task ports not implemented, RFC 9457 missing, no coverage evidence, no Docker/browser proof). Developer must address remediation items and resubmit before CEO review.

---

**Next Steps**:
- Developer: implement fixes + regenerate evidence.
- Owner: keep BLOCKER-001 open until validation succeeds.
