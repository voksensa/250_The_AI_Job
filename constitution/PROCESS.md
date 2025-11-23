# PROCESS.md — Task Execution & State Management

**Purpose**: This is the **single source of truth** for how work is done (task flow) and how state is tracked (INDEX, CURRENT_TASK, PROGRESS, BLOCKERS, DECISIONS).

---

## 1. What This Replaces

This document unifies the process parts of:

- `EXECUTION_PROTOCOL_SPEC.md` (how tasks are executed, gates, evidence)
- `STATE_MANAGEMENT.md` (state spine, persona startup protocols, handoffs)

Those two files remain as **reference** for detail, but **PROCESS.md is now law** for how CEO, Developer, and Researcher work and track state.

---

## 2. State Spine (Where "Truth" Lives)

The living state files are:

- `docs/state/INDEX.md` — Snapshot of where we are (phase, active task, top blockers).
- `docs/state/CURRENT_TASK.md` — Single active task with clear "Definition of Done".
- `docs/state/PROGRESS.md` — Chronological log of progress updates.
- `docs/state/BLOCKERS.md` — Current blockers with owner and date.
- `docs/state/DECISIONS_LOG.md` — (optional) Key decisions with links to evidence.

Rules:

1. INDEX is the **entry point**. If INDEX and other state files disagree, fix the others to match INDEX.  
2. There is **only one CURRENT_TASK at a time**. If you start a new one, close or archive the old.  
3. Every session MUST leave at least one line in PROGRESS or BLOCKERS.

---

## 3. Persona Startup Protocols (2-Minute Restore)

### 3.1 Developer Startup

1. Open `docs/state/INDEX.md` — current phase, task, blockers.  
2. Open `docs/state/CURRENT_TASK.md` — definition of done, gates in scope.  
3. Open `docs/state/BLOCKERS.md` — any blockers with `Owner: Dev`.  
4. Open `docs/state/PROGRESS.md` — last 3–5 entries for this task.  

Outcome: In <2 minutes, you know where we are and what to do next.

### 3.2 CEO Startup

1. Open `docs/state/INDEX.md`.  
2. Open `docs/state/CURRENT_TASK.md`.  
3. Open `docs/state/BLOCKERS.md` — any blockers with `Owner: CEO`.  
4. Skim evidence folders for gates in scope (G1–G11) as needed.

Outcome: In <2 minutes, you know what you are being asked to approve and what is blocking.

### 3.3 Researcher Startup

Same pattern, but focused on research tasks (`docs/research/…`) and G1/G2 evidence.

### 3.4 Validator Startup

1. Confirm you are the Validator for this pass.
2. Read `docs/state/INDEX.md`, `CURRENT_TASK.md`, `PROGRESS.md`, `BLOCKERS.md`.
3. Read the task file + linked evidence folders for the gates in scope.
4. Post a one-sentence summary of what you will validate; wait for the Owner’s YES before proceeding.

Outcome: In <2 minutes, you know scope, evidence, and whether you should proceed.

---

## 4. Task Execution Flow (Developer)

**For each TASK-… file:**

1. **Pre-Work**
   - Read the task file.  
   - Confirm it matches current phase in `INDEX.md`.  
   - Identify which gates (G1–G11) are in scope.  
   - Post a one-sentence understanding to Owner and wait for YES.

2. **Implementation**
   - Work in Docker from line 1.  
   - Keep backend + frontend in sync (Phase A+B together).  
   - Obey architecture patterns from `ARCHITECTURAL_DECISIONS.md`.  
   - Ensure new/changed code has ≥85% coverage.

3. **Evidence**
   - For each gate in scope, produce evidence under `evidence/G{N}/TASK-{ID}_...` according to templates.  
   - Capture Docker build/run logs and browser screenshots for user-visible features.

4. **Handoff**
   - Update `PROGRESS.md` and `CURRENT_TASK.md`.  
   - If blocked, log in `BLOCKERS.md` with `Owner: CEO` or `Owner: Owner`.  
   - Notify the Owner that the task is **ready for validation** (not approval).

(Details and examples live in `EXECUTION_PROTOCOL_SPEC.md` — this section is the contract.)

---

## 5. Validator Flow

After the Developer handoff:

1. Run the Validator startup protocol (3.4).
2. Check Golden Rules, Architecture Decisions, and gates using evidence only.
3. Write `docs/state/reports/VALIDATION_TASK-{ID}.md` with verdict (VALIDATED / REJECTED / CONDITIONAL) and any diamond risks.
4. Update `PROGRESS.md` (e.g., "Validation complete — VALIDATED") and `BLOCKERS.md` if remediation is required.
5. Notify Owner so they can decide whether to re-invoke Developer (for fixes) or move to CEO review.

---

## 6. CEO Review Flow

When CEO reviews a task:

1. Run Startup Protocol (3.2).  
2. Open the task file and evidence directories for gates in scope.  
3. Use the CEO Answer Format in `CLAUDE.md`:
   - Phase Context  
   - Golden Rules Check  
   - Evidence Review  
   - Decision (APPROVED / REJECTED / PARTIAL + next steps)

---

## 7. Relationship to Old Docs

- `EXECUTION_PROTOCOL_SPEC.md` — Detailed checklists per gate and role. Use as reference.  
- `STATE_MANAGEMENT.md` — Detailed definitions and examples for state files. Use as reference.

If there is **any conflict**, `PROCESS.md` wins.  
Update the old docs to match, or mark sections as deprecated.
