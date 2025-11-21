# EXECUTION PROTOCOL SPECIFICATION

## Executive Summary

This specification defines how any developer executes tasks for “Your First Engineer” with zero ambiguity and how CEOs verify quality via evidence instead of trust. It standardizes pre-work, implementation, testing, evidence capture, and handoff steps, and it defines a canonical evidence directory structure tied to quality gates G1–G11. The goal is to make every task reproducible, auditable, and automatable.

The protocol is tool-agnostic but assumes Git-based workflows, CI/CD, and the monorepo and state-management patterns defined in the architecture and state specs. Developers work from a **Task File + Gate Checklist**, produce evidence in `evidence/G*/`, and update living documents (`task.md`, `progress.md`, `blockers.md`). CEOs and Researchers use checklists mapped to each gate to approve or reject work based solely on evidence, enabling FAANG-style launch rigor for every change.

---

## 1. Design Goals & Non-Goals

### 1.1 Goals

1. **Deterministic Execution:** Given `{TASK_ID}`, any competent engineer can execute the task step-by-step without subjective interpretation.
2. **Evidence-First:** Every gate (G1–G11) has **named evidence artifacts** and pass/fail rules.
3. **Automatable:** CI can verify:
   - Required evidence files exist.
   - Lint/tests/coverage thresholds are met.
4. **Persona-Aligned:**
   - Developer: knows exactly what to do next.
   - CEO: can approve/reject based on clear, non-technical criteria.
   - Researcher: can add or refine gates and standards without changing code.

### 1.2 Non-Goals

- Replace human judgment: CEOs can still reject work that “feels wrong,” even if gates are technically green.
- Encode organization-specific HR or legal processes.

---

## 2. Developer Execution Protocol Template (RQ3)

Use this as a literal template (copy, fill `{PLACEHOLDER}`) for every task.

### 2.1 Task Metadata

Each task lives in a `TASK-{TASK_ID}.md` under `docs/tasks/` and starts with:

```markdown
# TASK-{TASK_ID}: {SHORT_TITLE}

- Phase: {PHASE_ID} (e.g., P1)
- Gates in Scope: {G1,G2,G4,G5,...}
- Owner: {OWNER_NAME}
- Developer: {DEV_NAME}
- Due Date: {YYYY-MM-DD}
- References:
  - Product: VISION.md, ROADMAP_SPEC.md
  - Architecture: COMPLETE_ARCHITECTURE_SPEC.md
  - State: STATE_MANAGEMENT_SPEC.md
  - Execution: EXECUTION_PROTOCOL_SPEC.md
  - Standards: NOVEMBER_2025_STANDARDS.md
````

### 2.2 Pre-Work Checklist

Developer MUST complete and tick this before writing code:

```markdown
## Pre-Work Checklist

[ ] Read TASK-{TASK_ID}.md top-to-bottom.
[ ] Open ROADMAP_SPEC.md and verify this task belongs to Phase {PHASE_ID}.
[ ] Open NOVEMBER_2025_STANDARDS.md and list applicable tools & thresholds.
[ ] Open STATE_MANAGEMENT_SPEC.md and confirm:
    - Current task is set in task.md.
    - progress.md reflects latest phase status.
[ ] Identify all gates in scope (e.g., G1, G2, G4, G5, G6, G9) and open corresponding README in evidence/.template/.
[ ] Create or update:
    - docs/state/task.md with TASK-{TASK_ID}.
    - docs/state/progress.md with initial estimate.
    - docs/state/blockers.md with any known risks.
[ ] Create a working branch: feature/TASK-{TASK_ID}-{slug}.
```

### 2.3 Implementation Steps

```markdown
## Implementation Steps

1. Design
   [ ] Sketch solution approach in TASK-{TASK_ID}.md under "Design Notes".
   [ ] If architecture changes: update ARCHITECTURE_CHANGE_LOG.md and prepare evidence/G2/ files.

2. Code
   [ ] Implement changes in smallest meaningful slices.
   [ ] Keep commits granular with messages: "TASK-{TASK_ID}: {change summary}".

3. Tests
   [ ] Add/extend unit tests for all new logic.
   [ ] Add/extend integration tests if behavior crosses service boundaries.
   [ ] Run local test suite (frontend + backend) until green.

4. Static Analysis
   [ ] Run lint (JS/TS and Python).
   [ ] Run type checks (TypeScript, mypy).
   [ ] Fix all errors and warnings; update task notes if trade-offs are taken.

5. Coverage
   [ ] Run coverage for touched modules.
   [ ] Ensure thresholds for new code and overall project are met.
   [ ] Generate HTML and/or XML reports to evidence/G5/.
```

### 2.4 Evidence Collection

```markdown
## Evidence Collection

For each gate in scope:

- G1 (Research)
  [ ] evidence/G1/TASK-{TASK_ID}-research-report.md
  [ ] evidence/G1/TASK-{TASK_ID}-sources.json

- G2 (Architecture)
  [ ] evidence/G2/TASK-{TASK_ID}-design.md
  [ ] evidence/G2/TASK-{TASK_ID}-diagram.mmd (Mermaid if needed)

- G3 (Security)
  [ ] evidence/G3/TASK-{TASK_ID}-threat-model.md
  [ ] evidence/G3/TASK-{TASK_ID}-sast-report.html (if applicable)

- G4 (Code Quality)
  [ ] evidence/G4/TASK-{TASK_ID}-lint.txt
  [ ] evidence/G4/TASK-{TASK_ID}-types.txt

- G5 (Testing & Coverage)
  [ ] evidence/G5/TASK-{TASK_ID}-pytest.txt (backend)
  [ ] evidence/G5/TASK-{TASK_ID}-frontend-tests.txt
  [ ] evidence/G5/TASK-{TASK_ID}-coverage-summary.txt
  [ ] evidence/G5/TASK-{TASK_ID}-coverage-html/ (directory or archive)

- G6 (Synthetic QA)
  [ ] evidence/G6/TASK-{TASK_ID}-synthetic-runs.json
  [ ] evidence/G6/TASK-{TASK_ID}-synthetic-report.md

- G7–G11
  [ ] Follow per-gate README under evidence/.template/G{N}/.
```

### 2.5 Handoff Steps (Developer → CEO)

```markdown
## Handoff Steps

[ ] Push branch and open PR: "TASK-{TASK_ID}: {SHORT_TITLE}".
[ ] Attach:
    - Link to TASK-{TASK_ID}.md.
    - Summary of changes (1–2 paragraphs).
    - List of gates in scope and evidence files created.
[ ] Update:
    - docs/state/progress.md with "Ready for CEO review" and link to PR.
    - docs/state/blockers.md (clear resolved blockers; highlight remaining).
[ ] Create session log:
    - logs/DEV/{YYYYMMDD-HHMM}-{TASK_ID}-{DEV_NAME}.md with:
      - Time spent.
      - Key decisions not obvious from code.
      - Open questions for CEO/Researcher.
```

---

## 3. Evidence Directory Structure (RQ3)

Canonical structure under monorepo root:

```text
evidence/
  .template/
    README.md
    G1/
      README.md
      TEMPLATE-research-report.md
      TEMPLATE-sources.json
    G2/
      README.md
      TEMPLATE-design.md
      TEMPLATE-diagram.mmd
    G3/
      README.md
      TEMPLATE-threat-model.md
      TEMPLATE-sast-report.md
    G4/
      README.md
      TEMPLATE-lint.txt
      TEMPLATE-types.txt
    G5/
      README.md
      TEMPLATE-pytest.txt
      TEMPLATE-frontend-tests.txt
      TEMPLATE-coverage-summary.txt
    G6/
      README.md
      TEMPLATE-synthetic-report.md
    G7/
      ...
    G8/
      ...
    G9/
      ...
    G10/
      ...
    G11/
      ...
  G1_Research/
  G2_Architecture/
  G3_Security/
  G4_CodeQuality/
  G5_TestingCoverage/
  G6_SyntheticQA/
  G7_ObservabilityReliability/
  G8_DataPrivacyCompliance/
  G9_AIRiskEthics/
  G10_UXAccessibility/
  G11_OperationalReadiness/
```

**Rules:**

* Evidence files use prefix: `TASK-{TASK_ID}-...`.
* CI checks:

  * For each open PR, determine `{TASK_ID}` and `gates in scope` from TASK file.
  * Validate required evidence files exist and are non-empty for those gates.
  * Fail PR if missing.

---

## 4. CEO Quality Gate Checklist

CEO uses these checklists to approve or reject tasks **without reading code**.

### 4.1 Usage

For each PR:

1. Open TASK file and note gates in scope.
2. For each gate, open corresponding evidence files.
3. Run gate-specific checklist; mark pass/fail.
4. Approve PR only if all gates pass or waivers are explicitly documented and justified.

### 4.2 Example Gate Checklists

**G4 – Code Quality**

* Inputs:

  * `evidence/G4/TASK-{TASK_ID}-lint.txt`
  * `evidence/G4/TASK-{TASK_ID}-types.txt`
* Checks:

  * [ ] Lint report shows “0 errors, 0 warnings” for ESLint and Ruff.
  * [ ] Type check report has no “error” entries.
  * [ ] Any rule suppressions (e.g., `eslint-disable`, `# noqa`) are justified in TASK file.
* Pass if all boxes checked; fail otherwise.

**G5 – Testing & Coverage**

* Inputs:

  * `pytest` and frontend test outputs.
  * `coverage` summary and HTML.
* Checks:

  * [ ] All tests pass (no failures, flakes documented).
  * [ ] New/modified backend code ≥80% line coverage.
  * [ ] New/modified frontend logic ≥70% line coverage.
  * [ ] Overall project coverage ≥60% (or higher if phase policy increases threshold).
* Pass if all thresholds met.

**G6 – Synthetic QA**

* Inputs:

  * Synthetic run JSON and report.
* Checks:

  * [ ] At least one happy-path and one negative-path synthetic journey executed.
  * [ ] No unresolved critical synthetic failures on core flows.
  * [ ] Any waivers are explicit, time-bounded, and justified.

(Additional gate-specific checklists are defined in `evidence/.template/G{N}/README.md`.)

---

## 5. Session Logs & State Updates

To align with STATE_MANAGEMENT_SPEC:

* Every working session (Dev, CEO, Researcher) creates a log under `logs/{ROLE}/`.
* Before ending a session, the person must:

  * Update `docs/state/task.md` with current active task or “None”.
  * Update `docs/state/progress.md` with current phase and status.
  * Add unresolved issues to `docs/state/blockers.md`.

This ensures any new persona can restore context in <2 minutes by:

1. Reading `STATE_MANAGEMENT_SPEC.md` startup protocol.
2. Checking `task.md`, `progress.md`, `blockers.md`.
3. Opening the latest log for their persona.

---

## 6. CEO & Researcher Protocols

### 6.1 CEO Approval Protocol

```markdown
1. Open STATE:
   [ ] Read docs/state/task.md and confirm TASK-{TASK_ID}.
   [ ] Read docs/state/progress.md for phase & status.

2. Open PR and TASK:
   [ ] Read TASK-{TASK_ID}.md summary and gates in scope.

3. Run Gate Checklists:
   [ ] For each gate, open evidence files and run per-gate checklist.
   [ ] Record decisions in evidence/G11/TASK-{TASK_ID}-gate-review.md.

4. Decide:
   [ ] Approve PR if all gates pass or waivers are justified.
   [ ] Or request changes with explicit failed checks.

5. Update STATE:
   [ ] Update docs/state/progress.md.
   [ ] Add any new blockers to blockers.md.
   [ ] Create CEO session log.
```

### 6.2 Researcher Protocol (Standards & Gating)

* For new standards:

  * Update `NOVEMBER_2025_STANDARDS.md`.
  * Update `.template` READMEs and templates for affected gates.
  * Add migration tasks (TASKs) if tools/thresholds change.

---

## 7. Integration with Quality Gates

Each gate is defined as:

```markdown
G{N}:
- Purpose: {short description}
- Tools: {tool list}
- Evidence: {required files}
- Thresholds: {pass/fail rules}
- Automation: {CI checks}
```

Details (tools, thresholds, automation) are specified in `NOVEMBER_2025_STANDARDS.md`. This protocol simply ensures **every task**:

1. Declares which gates it touches.
2. Produces the corresponding evidence.
3. Follows a consistent, automatable flow from Dev → CEO → Owner.

````
