# TASK-002 Pre-Flight Quality Configs

## Metadata

- **Task ID**: TASK-002_preflight-configs
- **Epic**: E001 – Foundation
- **Phase**: Phase 1 – MVP
- **Owner**: Developer
- **Status**: Done
- **Created**: 2025-11-21
- **Target Gates**: G3 (Lint Clean), G8 (Config Validated)
- **Related Decisions**:
  - [D-001] Next.js 16
  - [D-004] LangGraph 1.0.3
- **Inputs**:
  - [COMPLETE_ARCHITECTURE_SPEC.md](../../research/COMPLETE_ARCHITECTURE_SPEC.md)
  - [CLAUDE.md](../../constitution/CLAUDE.md)

## Problem Statement

Before Phase 1 feature development begins, we need to complete deferred quality gate configurations (ESLint for frontend, Docker Compose warning cleanup) to ensure all baseline quality standards are met.

## Constraints

From CEO mandate:
- Time box: 30 minutes maximum
- Must pass G3 (Lint Clean) and G8 (Config Validated)
- No feature work allowed until these configs are complete

## Plan

1. **ESLint Configuration (apps/web)**
   - Create `eslint.config.mjs` with strict Next.js rules
   - Add `lint` script to package.json
   - Run `npm run lint` - must pass with 0 errors

2. **Remove Docker Compose Warning**
   - Delete obsolete `version: '3.8'` line from docker-compose.yml

3. **Verification**
   - Run `npm run lint` in apps/web → 0 errors
   - Run `docker-compose up -d` → no version warnings
   - Verify services healthy (postgres + agent-runtime)

## Acceptance Criteria

- [ ] `apps/web/eslint.config.mjs` exists with strict config
- [ ] `npm run lint` in apps/web returns exit code 0
- [ ] `docker-compose.yml` has no `version:` line
- [ ] `docker-compose up -d` shows no warnings
- [ ] Health endpoint http://localhost:8002/health returns 200 OK
- [ ] Changes committed to Git

## Notes / Links

This completes the infrastructure hardening phase. After this task, we proceed to Phase 1 MVP (Production Toggle).
