# DECISIONS LOG

## Accepted

## D-015: Python Version Requirement (2025-11-21)
- **Decision**: Set `requires-python = ">=3.11"` (not ≥3.12)
- **Rationale**: NOVEMBER_2025_STANDARDS.md specifies "Python 3.11 minimum; prepare for 3.12 once all key tools fully support it"
- **Impact**: Allows broader environment compatibility while staying within spec
- **Alternatives Considered**: ≥3.12 (too restrictive), ≥3.10 (below spec minimum)
- **Owner**: CEO
- **Reference**: constitution/NOVEMBER_2025_STANDARDS.md line 50

## D-014: Ruff Adoption (2025-11-21)
- **Decision**: Add ruff ≥0.8.0 as primary linter/formatter, keep flake8 7.3.0 optional
- **Rationale**: Ruff is 10-100x faster, modern unified tool replacing black+flake8+isort. November 2025 industry standard.
- **Impact**: Faster CI, simpler toolchain, modern Python practices enforced
- **Alternatives Considered**: Keep only flake8+black (slower, multiple tools)
- **Owner**: CEO
- **Reference**: constitution/NOVEMBER_2025_STANDARDS.md §2.2

## D-013: Vitest 4.x for Frontend Testing (2025-11-21)
- **Decision**: Use Vitest 4.0.x instead of Jest for web app testing
- **Rationale**: October 2025 release with browser mode, better Next.js integration, faster than Jest
- **Impact**: Modern testing stack aligned with Vite/Next.js ecosystem
- **Alternatives Considered**: Jest 30.x (slower, less Vite-native)
- **Owner**: CEO
- **Reference**: constitution/NOVEMBER_2025_STANDARDS.md lines 38-44

## D-012: Tool Version Pinning Strategy (2025-11-21)
- **Decision**: Pin all dev tools to specific minor versions (e.g., pytest 9.0.x, ESLint 9.39.x)
- **Rationale**: Reproducible builds, avoid alpha/beta breakage (e.g., ESLint 10 alpha), align with NOVEMBER_2025_STANDARDS
- **Impact**: Stable CI, predictable developer experience, clear upgrade path
- **Alternatives Considered**: Use latest (unstable), use ranges (drift risk)
- **Owner**: CEO
- **Reference**: constitution/NOVEMBER_2025_STANDARDS.md §1

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
