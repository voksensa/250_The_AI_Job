# BLOCKERS

## Open

*None - B-005 resolved*

## Resolved

- **ID**: V-001
  - **Date**: 2025-11-21
  - **Resolution**: Implemented missing `routes.py` and `graph.py` with native LangGraph patterns.
  - **Task**: TASK-FIX-001
  - **Evidence**: Service running, health check passing, session log created.

- **ID**: B-005
  - **Date**: 2025-11-21  
  - **Resolution**: Used Python 3.12 from /opt/homebrew/bin, created venv, all tools verified working
  - **Task**: Phase 0 - Tool Version Verification
  - **Evidence**: 
    - Python 3.12 venv at apps/agent-runtime/.venv
    - pytest 9.0.1, mypy 1.18.2, ruff 0.14.6, coverage 7.12.0 installed
    - All lint + type checks pass (commits 43d4968, [latest])

- **ID**: B-004
  - **Date**: 2025-11-21
  - **Resolution**: Research brief completed by Owner's researcher. Framework implementation complete.
  - **Task**: Phase 0
  - **Severity**: CRITICAL
  - **Description**: Must define execution framework, roadmap, and November 2025 standards before ANY development work proceeds.
