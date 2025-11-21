# BLOCKERS

## Open

_No open blockers._

## Resolved

- **ID**: B-003
  - **Date**: 2025-11-21
  - **Task**: Infrastructure Hardening
  - **Owner**: Researcher
  - **Severity**: High
  - **Type**: Research
  - **Description**: Define state management system to prevent Goldfish Memory problem.
  - **Status**: Resolved on 2025-11-21 (see Decision D-010, STATE_MANAGEMENT_SPEC.md delivered).

- **ID**: B-002
  - **Date**: 2025-11-21
  - **Task**: Infrastructure Hardening
  - **Owner**: Developer
  - **Severity**: Critical
  - **Type**: Dependency
  - **Description**: LangGraph version drift - spec requires 1.0.3, installed 0.2.59.
  - **Status**: Resolved on 2025-11-21 (removed conflicting packages, verified langgraph==1.0.3 installed).

- **ID**: B-001
  - **Date**: 2025-11-21
  - **Task**: Infrastructure Hardening
  - **Owner**: Developer
  - **Severity**: High
  - **Type**: Configuration
  - **Description**: Docker build failures due to dependency resolution conflicts.
  - **Status**: Resolved on 2025-11-21 (pinned exact versions, build time: 26s).
