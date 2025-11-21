# BLOCKERS

## Open

- **ID**: B-005
  - **Date**: 2025-11-21
  - **Blocker**: Python 3.9.6 found, need ≥3.11 for agent-runtime
  - **Task**: Phase 0 - Tool Version Verification
  - **Severity**: LOW (code correct, verification pending)
  - **Description**: 
    - System Python: 3.9.6 (Xcode)
    - Required: ≥3.11 (per NOVEMBER_2025_STANDARDS.md + pyproject.toml)
    - Checked: /usr/local/bin, /opt/homebrew/bin - no Python 3.11+ found
  - **Impact**: Cannot verify Python tool installations (pytest, mypy, ruff, coverage)
  - **Resolution Options**:
    1. **Install Python 3.11+**: `brew install python@3.11` or `brew install python@3.12`
    2. **Defer to Docker**: Verify in Docker container (has Python 3.11+ base image)
    3. **Defer to CI**: Let CI pipeline verify on push
  - **Recommendation**: Option 2 (Docker) - most aligned with production environment
  - **Status**: AWAITING OWNER DECISION

## Resolved

- **ID**: B-004
  - **Date**: 2025-11-21
  - **Resolution**: Research brief completed by Owner's researcher. Framework implementation complete.
  - **Task**: Phase 0
  - **Severity**: CRITICAL
  - **Description**: Must define execution framework, roadmap, and November 2025 standards before ANY development work proceeds.
