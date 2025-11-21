# DECISIONS LOG

## Accepted

- **[D-010]** 2025-11-21 – **State Management Framework**
  - **Summary**: Adopt repo-based state management with living documents (INDEX, CURRENT_TASK, PROGRESS, BLOCKERS, DECISIONS_LOG).
  - **Rationale**: Eliminates "Goldfish Memory" problem with minimal overhead; ADR-style immutable decisions; persona-specific startup protocols.
  - **Supersedes**: None.
  - **Evidence**: [STATE_MANAGEMENT_SPEC.md](../research/STATE_MANAGEMENT_SPEC.md), [evidence/G2/state-management-decisions.json](../../evidence/G2/state-management-decisions.json)

- **[D-004]** 2025-11-21 – **Stack.orchestration**
  - **Summary**: LangGraph 1.0.3 selected as orchestration framework.
  - **Rationale**: Native v1.0.3 patterns per COMPLETE_ARCHITECTURE_SPEC.md line 151; Postgres checkpointer 3.0.x for production persistence.
  - **Supersedes**: None.
  - **Evidence**: [COMPLETE_ARCHITECTURE_SPEC.md](../research/COMPLETE_ARCHITECTURE_SPEC.md), verified via `pip list` in docker container.

- **[D-003]** 2025-11-21 – **Stack.backend_runtime**
  - **Summary**: Python 3.12.x selected as backend runtime.
  - **Rationale**: Balance between maturity and longevity; mainstream support; good performance; low ecosystem risk.
  - **Supersedes**: None.
  - **Evidence**: [COMPLETE_ARCHITECTURE_SPEC.md](../research/COMPLETE_ARCHITECTURE_SPEC.md) section 2.4.

- **[D-002]** 2025-11-21 – **Stack.css**
  - **Summary**: Tailwind CSS 4.0+ selected as CSS framework.
  - **Rationale**: Latest stable major version; performance improvements; modern DX; aligns with Next.js 16.
  - **Supersedes**: None.
  - **Evidence**: [COMPLETE_ARCHITECTURE_SPEC.md](../research/COMPLETE_ARCHITECTURE_SPEC.md) section 2.2.

- **[D-001]** 2025-11-21 – **Stack.frontend**
  - **Summary**: Next.js 16.0.x selected as frontend framework.
  - **Rationale**: Current major line; App Router maturity; React Compiler; Turbopack benefits; strong ecosystem.
  - **Supersedes**: None.
  - **Evidence**: [COMPLETE_ARCHITECTURE_SPEC.md](../research/COMPLETE_ARCHITECTURE_SPEC.md) section 2.1.

## Superseded

_No superseded decisions yet._
