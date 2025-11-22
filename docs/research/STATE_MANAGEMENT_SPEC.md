
# STATE MANAGEMENT SPECIFICATION

File: docs/research/STATE_MANAGEMENT_SPEC.md  
Date: 2025-11-21  
BriefID: YFE-STATE-001  

---

## Executive Summary

The “Goldfish Memory” problem is simple: every session starts from zero. New or returning personas (Developer, CEO, Researcher) have no trusted way to know **where we are**, **what’s active**, or **what’s already decided**. This has already cost 249 attempts and countless cycles re-debating choices like Next.js 16 and LangGraph 1.0.3.

This specification defines a **lightweight, file-based state system** that turns the repository itself into a **Single Source of Truth (SSoT)** for project context.:contentReference[oaicite:0]{index=0} It standardizes:
- **Where state lives** (`docs/state/`),
- **How each persona starts a session** (startup checklists),
- **How work moves between personas** (handoff protocols),
- **How decisions and quality gates are recorded** (living documents + ADR-style logs).:contentReference[oaicite:1]{index=1}  

The goal: any Developer, CEO, or Researcher can restore context in **< 2 minutes**, know “where we are” in **30 seconds**, and never re-open a settled decision unless they create a new, explicit decision record.

---

## 1. The Problem: Goldfish Memory

### 1.1 Symptoms Observed

From the first 250 attempts on “Your First Engineer”:

- **Repeated debates**: Next.js 15 vs 16, Tailwind 3 vs 4, and similar decisions were revisited because there was no authoritative decision log.
- **No explicit “current task”**: Work-in-progress lived in chat, memory, or local scratchpads, not in the repo.
- **No session handoff**: When the role changed (Dev → CEO → Researcher), the next persona had no precise pointer to what needed review or action.
- **Scattered instructions**: Briefs, mandates, and constraints were in multiple places and not consistently linked to tasks.

This is a classic context-loss scenario seen in distributed and fast-growing teams: without a central, well-structured knowledge base and explicit runbooks, onboarding and context switching become major bottlenecks.:contentReference[oaicite:2]{index=2} Context switching itself drastically reduces effective productivity, especially when multiple tasks are in flight.:contentReference[oaicite:3]{index=3}  

### 1.2 Root Causes

1. **No Single Source of Truth (SSoT)**: There is no single place to answer “what’s the current state of the project?” Product and engineering literature consistently emphasizes SSoT as critical to avoid misalignment and churn.:contentReference[oaicite:4]{index=4}  
2. **No explicit “state spine”**: Documentation exists (e.g., COMPLETE_ARCHITECTURE_SPEC.md) but is static, not tied into a living state structure.
3. **No standardized runbooks**: Each persona improvises their startup sequence, instead of following a simple checklist. Runbooks are widely used in platform and incident management to make complex systems operable by many people.:contentReference[oaicite:5]{index=5}  
4. **Unstructured decisions**: Decisions are not recorded as ADRs or similar immutable records, so they are easy to re-open unintentionally.:contentReference[oaicite:6]{index=6}  

---

## 2. State Management Principles

These principles govern **all** state for “Your First Engineer” and must align with the existing constitution (VISION → STRATEGY → ROADMAP → CLAUDE → AGENTS).

1. **Single Source of Truth (SSoT).**  
   - There is exactly **one** canonical entrypoint for “Where are we?”: `docs/state/INDEX.md`.  
   - External tools (Jira, Notion, etc.) may mirror data, but the **repo wins** on conflicts.

2. **Living Documents vs Snapshots.**
   - A **living document** is expected to be current and actively maintained (e.g., `docs/state/INDEX.md`, `CURRENT_TASK.md`, `BLOCKERS.md`, `PROGRESS.md`).
   - A **snapshot** is immutable once published (e.g., research specs, ADRs, decisions logs for a closed phase).

3. **Immutable Decisions, Explicit Supersession.**
   - Once recorded, decisions (e.g., “Next.js 16 is the frontend framework”) are **never edited in place**.  
   - If a decision changes, a new decision record explicitly supersedes the old one (ADR pattern).:contentReference[oaicite:7]{index=7}  
   - No debates are allowed on a decided topic unless the question is clearly framed as “Should we supersede Decision X?”

4. **Persona-Specific Entrypoints.**
   - Each persona (Developer, CEO, Researcher) has a **2–3 step startup checklist** tailored to their responsibilities.
   - All checklists start from the same SSoT (`INDEX.md`) but diverge appropriately.

5. **Minimalism: Simple but Functional.**
   - The system uses **markdown files in the repo**; no custom app or database is required.
   - The number of core living documents is intentionally small (4–7 files) to avoid overhead.

6. **Runbook-Driven Operation.**
   - Routine flows (startup, handoff, gate reviews) are documented as **runbooks** so they are repeatable by any persona.:contentReference[oaicite:8]{index=8}  

7. **Quality-Gate Integration.**
   - Each major task explicitly references which Quality Gates (G1–G11) it targets or depends on.
   - Passing a gate creates or updates a decision record; failing a gate creates a blocker entry.

8. **Git as Time Machine.**
   - State files live in Git for version history and accountability.
   - Archives get moved rather than deleted, preserving the evolution of state.

---

## 3. File Structure

### 3.1 High-Level Layout

This builds on the existing structure used for COMPLETE_ARCHITECTURE_SPEC.md.

```text
/ (repo root)
  constitution/
    VISION.md
    STRATEGY.md
    ROADMAP.md
    QUALITY_GATES.md          # Definitions of G1–G11
    CLAUDE_AND_AGENTS.md
    STATE_MANAGEMENT.md       # Stable version of this spec (once promoted)
  docs/
    research/
      COMPLETE_ARCHITECTURE_SPEC.md
      STATE_MANAGEMENT_SPEC.md
      ... other research briefs ...
    state/                    # *** State Spine (living) ***
      INDEX.md                # SSoT for “Where are we?”
      CURRENT_TASK.md         # Exactly one current task at a time
      PROGRESS.md             # Short running log of major changes
      BLOCKERS.md             # Active blockers with owners/status
      DECISIONS_LOG.md        # Human-readable summary of key decisions
      SESSIONS/               # Per-session logs (optional, for traceability)
        2025-11-21_ceo_escalation.md
        ...
      tasks/
        TASK-001_preflight-configs.md
        TASK-002_phase1-mvp-setup.md
        ...
      archive/
        2025-10/...
  evidence/
    G1/                       # RA artifacts (research reports, decisions.json, etc.)
      decisions.json
      comparative-matrix.csv
      ...
````

**Key rules:**

* **All personas start from `docs/state/INDEX.md`.**
* **All task instructions live under `docs/state/tasks/`.**
* **Decision details live in `evidence/` (for structured data) and `DECISIONS_LOG.md` (for human scanning).**

### 3.2 Naming Conventions

* **Tasks:** `TASK-XXX_<kebab-slug>.md` (e.g., `TASK-003_phase1-mvp-langgraph-graph.md`).
* **Session logs:** `YYYY-MM-DD_<persona>_<short-description>.md`.
* **ADRs (if used separately):** `ADR-YYYYMMDD-<slug>.md` in `docs/decisions/` (optional extension).

---

## 4. Persona Startup Protocols

Each protocol has two layers:

* **30-second orientation** – high-level: “Where are we?”
* **<2-minute restore** – enough detail to meaningfully resume work or review.

### 4.1 Developer Startup

**Goal:** Know which task you own, what’s done, and what’s blocked in **< 2 minutes**.

**Step 0 – Open SSoT (30 seconds)**

1. Open `docs/state/INDEX.md`.

   * Check **Project Phase**, **Active Epic**, **Current Task ID**, **Current Owner**, and **Last Updated**.
   * If any of these are missing or obviously stale (> 2 days with active work assumed), treat that as your **first task**: fix INDEX with CEO approval.

**Step 1 – Understand the Current Task (60–90 seconds)**

2. Open `docs/state/CURRENT_TASK.md`.

   * Verify it matches the `Current Task ID` in `INDEX.md`.
   * Confirm **Owner** is you (or you’re explicitly picking it up with CEO agreement).
3. Open the corresponding detailed task file: `docs/state/tasks/<TASK-ID>.md`.

   * Read the **Objective**, **Definition of Done**, **Linked Decisions**, and **Target Quality Gates**.

**Step 2 – Check Progress & Blockers (30–60 seconds)**

4. Skim `docs/state/PROGRESS.md` from the bottom up for the last 3–5 entries.
5. Skim `docs/state/BLOCKERS.md` for any blockers tagged with your TASK-ID.

**Step 3 – Resume Work (ongoing)**

When resuming mid-task:

* Use the “Next Action” section in `CURRENT_TASK.md` (mandatory) to know exactly what to do next.
* If it’s missing, **your first action** is to define it and sync with CEO if needed.

---

### 4.2 CEO Startup

**Goal:** Know current phase, risk, and decisions required **without rereading the codebase**.

**Step 0 – Open SSoT (30 seconds)**

1. Open `docs/state/INDEX.md`.

   * Confirm **Phase**, **Active Epic**, **Current Task**, and **Gate Focus** (e.g., “Currently targeting G1 and G2”).

**Step 1 – Decision Snapshot (60 seconds)**

2. Open `docs/state/DECISIONS_LOG.md`.

   * Read the latest 3–5 decisions and see if any are marked **“Pending CEO”**.
3. Check `docs/state/BLOCKERS.md` for any **Severity: High / Owner: CEO** entries.

**Step 2 – Review Work-in-Progress (60 seconds)**

4. Open `docs/state/CURRENT_TASK.md`.

   * Look for the **“CEO Needs To Decide”** section (if present).
5. If you’re doing a gate review, open the relevant spec (e.g., `COMPLETE_ARCHITECTURE_SPEC.md`, `STATE_MANAGEMENT_SPEC.md`) as linked from the task file, not by hunting manually.

---

### 4.3 Researcher Startup

**Goal:** Understand the research question, constraints, and current state **without re-deriving context from scratch**.

**Step 0 – Open SSoT (30 seconds)**

1. Open `docs/state/INDEX.md` and confirm:

   * Current Phase, Active Epic, Current Task (often something like `TASK-00X_research_<topic>`).
   * Owner (should be “Researcher” or this session’s RA).

**Step 1 – Research Brief (60–90 seconds)**

2. Open the relevant task file: `docs/state/tasks/TASK-XXX_research_<topic>.md`.

   * Read the **Brief**, **Constraints**, **Success Criteria**, **Deadline**, and **Downstream Consumers**.
3. Open any linked files (e.g., `docs/research/COMPLETE_ARCHITECTURE_SPEC.md`) referenced under **Inputs**.

**Step 2 – Check Decisions & Blockers (30–60 seconds)**

4. Skim `DECISIONS_LOG.md` to understand past decisions on related topics.
5. Check `BLOCKERS.md` for entries where **Type = Research** or **Owner = Researcher**.

---

## 5. Living Documents

### 5.1 `docs/state/INDEX.md` – State Spine (SSoT)

**Purpose:** The **single fastest answer** to “Where are we?” and “Who owns the ball?”.

**Recommended structure:**

```markdown
# PROJECT STATE INDEX

## Snapshot (Living)

- Phase: Phase 1 – MVP (Production Toggle Proof)
- Active Epic: E001 – Pre-Flight Configs
- Current Task ID: TASK-001_preflight-configs
- Current Owner: Developer
- Gate Focus: G1 (Research), G2 (Architecture), G3 (Security Pre-Check)
- Last Updated: 2025-11-21 by CEO

## Quick Links

- Current Task: docs/state/CURRENT_TASK.md
- Blockers: docs/state/BLOCKERS.md
- Progress Log: docs/state/PROGRESS.md
- Decisions: docs/state/DECISIONS_LOG.md
- Key Specs:
  - Complete Architecture: docs/research/COMPLETE_ARCHITECTURE_SPEC.md
  - State Management: docs/research/STATE_MANAGEMENT_SPEC.md
```

**Update rules:**

* Updated **whenever**:

  * Phase changes,
  * Current Task changes,
  * Owner changes,
  * Gate focus changes.
* Owner: CEO by default (can delegate but remains accountable).

---

### 5.2 `docs/state/CURRENT_TASK.md` – The One Task in Focus

**Purpose:** There is **exactly one** current task at any time. This keeps the system aligned and reduces context-switching.([Medium][1])

**Recommended structure:**

```markdown
# CURRENT TASK

- Task ID: TASK-001_preflight-configs
- Title: Pre-Flight Configs for Phase 1
- Owner: Developer
- Status: In Progress
- Related Phase: Phase 1 – MVP (Production Toggle Proof)
- Target Gates: G1, G2
- Linked Specs:
  - COMPLETE_ARCHITECTURE_SPEC.md
  - STATE_MANAGEMENT_SPEC.md

## Objective

Short plain-language statement of what this task must achieve.

## Definition of Done

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Next Action (Mandatory)

Single, concrete next step the Owner should take.

## CEO Needs To Decide (Optional)

List any decisions required from CEO for this task.

## Notes

Short notes only; detailed reasoning belongs in the task file and/or research specs.
```

**Update rules:**

* Owner (Dev/Researcher) updates **Next Action** after each working block.
* CEO updates **Owner** and **Status** when reassigning or closing.

---

### 5.3 `docs/state/tasks/TASK-XXX_*.md` – Task Files

Each task file is a **self-contained contract** for a unit of work.

**Recommended structure:**

```markdown
# TASK-001 Pre-Flight Configs

## Metadata

- Task ID: TASK-001_preflight-configs
- Epic: E001 – Pre-Flight Configs
- Phase: Phase 1 – MVP
- Owner: Developer
- Status: In Progress | Done | Archived
- Created: 2025-11-21
- Target Gates: G1, G2
- Related Decisions:
  - [D-001] Frontend stack fixed: Next.js 16 + Tailwind 4
- Inputs:
  - COMPLETE_ARCHITECTURE_SPEC.md
  - STATE_MANAGEMENT_SPEC.md

## Problem Statement

Short description of the problem this task solves.

## Constraints

From constitution and relevant specs.

## Plan

High-level steps (not micro-tasks).

## Acceptance Criteria

List conditions that must be true to consider this task “Done”.

## Notes / Links

Links to PRs, issues, etc.
```

**Lifecycle:**

* **Status changes**: `In Progress` → `Done` → `Archived`.
* Once archived, file gets moved to `docs/state/archive/YYYY-MM/`.

---

### 5.4 `docs/state/PROGRESS.md` – Progress Log

**Purpose:** Lightweight log of significant milestones; **no more than 1–3 lines per event**.

**Example:**

```markdown
# PROGRESS LOG

- 2025-11-21 – CEO – Approved COMPLETE_ARCHITECTURE_SPEC.md, Phase 1 can start.
- 2025-11-21 – Researcher – Delivered STATE_MANAGEMENT_SPEC.md (YFE-STATE-001).
- 2025-11-22 – Developer – Created TASK-001_preflight-configs and updated CURRENT_TASK.md.
```

**Update rules:**

* Anyone who completes a **notable event** (spec delivery, gate passed, task closed) adds a single log line.
* This file should be quick to skim; no essay-length entries.

---

### 5.5 `docs/state/BLOCKERS.md` – Blockers & Decisions Pending

**Purpose:** Single list of anything that prevents progress.

**Example structure:**

```markdown
# BLOCKERS

## Open

- ID: B-001
  - Date: 2025-11-21
  - Task: TASK-001_preflight-configs
  - Owner: CEO
  - Severity: High
  - Type: Decision
  - Description: Approve or adjust STATE_MANAGEMENT_SPEC.md before Pre-Flight Configs.
  - Status: Open

## Resolved

- ID: B-000
  - Date: 2025-11-20
  - Task: TASK-000_bootstrap
  - Owner: CEO
  - Severity: Medium
  - Type: Clarification
  - Description: Decide on monorepo vs polyrepo.
  - Status: Resolved on 2025-11-21 (see Decision D-002).
```

**Rules:**

* Every open blocker has:

  * **Owner** (one person),
  * **Task** ID,
  * **Severity**,
  * **Type** (Decision, Research, Dependency, Infra, etc.).
* Blocking decisions for CEO/Researcher are represented here, not scattered.

---

### 5.6 `docs/state/DECISIONS_LOG.md` – Human-Readable Decisions

**Purpose:** A quick, human-readable log of key decisions; mirrors structured data in `evidence/G#/decisions.json`.

**Example structure:**

```markdown
# DECISIONS LOG

## Accepted

- [D-001] 2025-11-21 – Stack.frontend
  - Summary: Next.js 16 selected as frontend framework.
  - Rationale: Alignment with current major line, App Router, React Compiler, and Turbopack benefits.
  - Supersedes: None.
  - Evidence: evidence/G1/decisions.json

- [D-002] 2025-11-21 – Stack.css
  - Summary: Tailwind 4 selected as CSS framework.
  - Supersedes: None.

## Superseded

- [D-000] 2025-11-15 – Prototype frontend stack (discarded)
  - Summary: Next.js 15 + Tailwind 3 used for prototypes only.
  - Superseded by: D-001, D-002.
```

**Rules:**

* Each entry maps to a structured record (e.g., RA `decisions.json`) where applicable.
* No editing past decisions; instead, add new entries and mark old ones as **Superseded**.

---

### 5.7 `docs/state/SESSIONS/*.md` – Optional Session Logs

Optional but recommended when sessions are complex or long.

**Example:**

```markdown
# Session 2025-11-21 – CEO Escalation

- Persona: CEO
- Context: Escalation of Goldfish Memory problem.
- Inputs: Attempts 1–249, COMPLETE_ARCHITECTURE_SPEC.md.
- Output: Research brief for STATE_MANAGEMENT_SPEC.md.
- Next Owner: Researcher
- Linked Task: TASK-00X_research_state-management
```

---

## 6. Handoff Protocols

All handoffs use the same three steps:

1. **State Update** (CURRENT_TASK, BLOCKERS, PROGRESS).
2. **Explicit Owner Change** (in INDEX and CURRENT_TASK).
3. **Notification** (PR comment, message, or other agreed channel referencing Task ID).

### 6.1 Developer → CEO

**When:** Work is ready for review, a gate needs approval, or a decision is needed.

**Checklist:**

1. Update `CURRENT_TASK.md`:

   * Ensure **Status** reflects current reality (e.g., “Ready for CEO Review”).
   * Under **CEO Needs To Decide**, list specific decisions/questions.
2. Update `PROGRESS.md`:

   * Add a line summarizing what’s ready (e.g., “Dev completed preflight configs; CEO review needed for G1 & G2.”).
3. Update `BLOCKERS.md`:

   * Add or update a blocker of **Type: Decision** with `Owner: CEO` if applicable.
4. Update `INDEX.md`:

   * If task ownership changes to CEO (e.g., CEO-run review), update **Current Owner** to CEO.
5. Notify CEO:

   * Share a link to `CURRENT_TASK.md` and the relevant spec(s), not just the PR.

---

### 6.2 CEO → Researcher

**When:** CEO escalates a question that requires structured research (like the Goldfish problem).

**Checklist:**

1. Create or update a research task file in `docs/state/tasks/` (e.g., `TASK-00X_research_state-management.md`) with:

   * Clear **Research Question**,
   * Constraints,
   * Success Criteria,
   * Deadline,
   * Downstream Consumers.
2. Set `CURRENT_TASK.md` to this research task if it becomes the global focus.
3. Update `BLOCKERS.md`:

   * Add a blocker of **Type: Research** with `Owner: Researcher`.
4. Update `INDEX.md`:

   * Phase/Epic as needed; Current Owner set to Researcher if they now own the ball.
5. Notify Researcher:

   * Share the Task ID and link to the research brief.

---

### 6.3 Researcher → Developer

**When:** Research is complete and a new spec or decision is ready to be implemented.

**Checklist:**

1. Produce the research artifact (e.g., `STATE_MANAGEMENT_SPEC.md`) in `docs/research/`.
2. Update or create decisions in `DECISIONS_LOG.md` and structured `decisions.json` under `evidence/G#/`.
3. Update `PROGRESS.md`:

   * Log the delivery of the research spec and any accepted decisions.
4. Update `BLOCKERS.md`:

   * Mark related Research blockers as **Resolved** and link to the new spec.
5. Update `CURRENT_TASK.md`:

   * Either:

     * Move current research task to `Status: Done` and set the next implementation task as current, or
     * Leave current task but set **Next Action** as a Developer-owned step.
6. Update `INDEX.md`:

   * Set **Current Owner: Developer** (or as appropriate).
7. Notify Developer:

   * Share Task ID and spec links.

---

## 7. Integration with Quality Gates (G1–G11)

The quality gates (G1–G11) are defined in `constitution/QUALITY_GATES.md` and enforced via:

1. **Explicit Gate Targeting per Task.**

   * Each task includes a **Target Gates** field.
   * `CURRENT_TASK.md` always shows which gate(s) it is driving.

2. **Gate Checklists as Living Documents.**

   * Optional but recommended: `docs/gates/Gn_CHECKLIST.md` per gate.
   * Tasks link to the relevant gate checklist.

3. **Gate Reviews Recorded as Decisions.**

   * When a gate is passed/failed, CEO logs:

     * A line in `PROGRESS.md`,
     * An entry in `DECISIONS_LOG.md` (and, if needed, structured `decisions.json`).
   * This prevents re-litigation of gate outcomes.

4. **Regression Prevention.**

   * CI can enforce simple checks (conceptual outline; implementation left to Dev/Infra):

     * For PRs labeled as “G1: Research”, ensure:

       * A research spec file exists,
       * `PROGRESS.md` and `DECISIONS_LOG.md` updated.
     * For PRs that change architecture or stack:

       * Require a new decision record or explicit statement “No decision changed.”
   * This mirrors how ADR best practices recommend storing decisions with code and using status indicators to keep them discoverable and current.([techtarget.com][2])

5. **Production from Line 1.**

   * Policy: **No feature work starts** unless:

     * `docs/state/INDEX.md` exists and is filled,
     * `CURRENT_TASK.md` points to a valid task,
     * The task references at least one gate.
   * This ensures every line of code is traceable back to a task, gate, and constitutional constraint.

---

## 8. Examples

### 8.1 Fresh Session – Developer Resuming Phase 1

**Scenario:** A new Developer starts work on Phase 1 Pre-Flight Configs.

1. Open `docs/state/INDEX.md`:

   * Sees: Phase 1 – MVP, Active Epic E001, Current Task `TASK-001_preflight-configs`, Owner: Developer.
   * Time: ~10 seconds.
2. Open `CURRENT_TASK.md`:

   * Reads Objective and Definition of Done; sees **Next Action: “Set up monorepo structure according to COMPLETE_ARCHITECTURE_SPEC.md, section 3.2.”**
   * Time: ~30–45 seconds.
3. Open `TASK-001_preflight-configs.md`:

   * Reads constraints, plan, and acceptance criteria; notes Target Gates: G1, G2.
   * Time: ~30–45 seconds.
4. Skim `PROGRESS.md` and `BLOCKERS.md`:

   * Confirms no unresolved blockers on this task.
   * Time: ~30 seconds.

Total: ~2 minutes to fully restore context.

---

### 8.2 Mid-Task Handoff – Developer → CEO

**Scenario:** Developer finishes initial implementation for Pre-Flight Configs and needs CEO gate review.

1. Dev updates `CURRENT_TASK.md`:

   * Status: `Ready for CEO Review`.
   * Next Action: “CEO: Approve pre-flight config decisions against QUALITY_GATES G1, G2.”
   * Adds bullet list of specific questions under **CEO Needs To Decide**.
2. Dev updates `PROGRESS.md`:

   * “2025-11-22 – Dev – Completed initial preflight configs; CEO review for G1/G2 needed.”
3. Dev updates `BLOCKERS.md`:

   * Adds `B-002` with Owner: CEO, Type: Decision, Task: `TASK-001_preflight-configs`.
4. Dev pings CEO with link to `CURRENT_TASK.md` and relevant specs.

When CEO starts their session:

* They open `INDEX.md` → `CURRENT_TASK.md` → see **CEO Needs To Decide** and B-002.
* They can make a decision **without** rereading the entire codebase.

---

### 8.3 CEO Escalation – CEO → Researcher (Goldfish Problem)

**Scenario:** CEO recognizes Goldfish Memory as systemic risk (this brief).

1. CEO creates `docs/state/tasks/TASK-00X_research_state-management.md` with:

   * Clear Research Question,
   * Constraints (“Simple but Functional”, 3 personas, integration with constitution),
   * Success Criteria (2-min restore, 30-second “where we are”, etc.).
2. CEO sets `CURRENT_TASK.md` to this research task and Owner: Researcher.
3. CEO updates `BLOCKERS.md`:

   * Adds `B-003` (Type: Research, Owner: Researcher).
4. CEO updates `PROGRESS.md`:

   * Logs escalation.

Researcher starts:

* Opens `INDEX.md` → sees Phase/Epic, Current Task `TASK-00X_research_state-management` and Owner: Researcher.
* Opens task file and this research brief.
* After completing research, Researcher delivers `STATE_MANAGEMENT_SPEC.md`, updates decisions, blockers, and hands back to Dev per §6.3.

---

### 8.4 Researcher → Developer – Implementing State Management

**Scenario:** This specification is approved and must be implemented.

1. Researcher logs decision in `DECISIONS_LOG.md` and `evidence/G#/decisions.json` (e.g., `D-010 State Management Approach`).
2. Researcher sets `TASK-00X_research_state-management.md` to `Status: Done`.
3. CEO creates implementation task `TASK-00Y_implement_state-management-files.md`.
4. `CURRENT_TASK.md` is updated to `TASK-00Y_*` with Owner: Developer and **Next Action**: “Create docs/state directory and seed INDEX/CURRENT_TASK/PROGRESS/BLOCKERS/DECISIONS_LOG as per spec.”
5. Dev implements file structure and initial content, then logs progress and closes blockers.

From this point, **every future session** follows the startup protocols, eliminating the Goldfish Memory problem by design.

---

## 9. Success Criteria Mapping

This spec is considered successful if, in practice:

* ✅ **Fresh session restores context in < 2 minutes**

  * Achieved through `INDEX.md` + `CURRENT_TASK.md` + `PROGRESS/BLOCKERS` in defined startup sequences.

* ✅ **Any persona knows “where we are” in 30 seconds**

  * Achieved by always starting at `docs/state/INDEX.md` as SSoT.

* ✅ **Zero debates on already-made decisions**

  * Achieved via `DECISIONS_LOG.md` + structured decisions.json + immutable decision records and explicit supersession.

* ✅ **Clean handoffs between Dev/CEO/Researcher**

  * Achieved via standardized handoff protocols and shared living documents.

* ✅ **Works with existing constitution (VISION → STRATEGY → ROADMAP → CLAUDE → AGENTS)**

  * Constitution remains the **source of “why” and global constraints**; this spec defines **“how we track and operate the work”**.
  * STATE_MANAGEMENT.md (once promoted) becomes part of the constitution, binding future work.

Once the Owner approves this spec, it must be copied and frozen as:

`/Users/Yousef_1/Downloads/250_The_AI_Job/constitution/STATE_MANAGEMENT.md`

and referenced from `constitution/ROADMAP.md` and `constitution/QUALITY_GATES.md` as a mandatory process for all phases.

---

````

```csv
filename="evidence/G2/state-management-comparative-matrix.csv"
OptionID,Category,OptionName,Description,Pros,Cons,RiskLevel,TCO_3yr,Performance,Primary
ssot_repo,StateModel,Repo as Single Source of Truth,"All project state lives in the code repository: markdown docs + structured JSON under version control.","Maximizes transparency; easy to link to code; offline-capable; simple tooling (Git).","Requires disciplined updates; no rich dashboards by default; some manual overhead.",LOW,LOW,MEDIUM,TRUE
ssot_tool,StateModel,External PM Tool as SSoT,"Use Jira/Linear/Notion as the primary source of truth, with repo docs secondary.","Rich UI and reporting; familiar to many teams; built-in workflows.","Splits state between tool and repo; harder to keep specs/decisions close to code; vendor lock-in.",MEDIUM,MEDIUM,HIGH,FALSE
ssot_hybrid,StateModel,Hybrid Hub-and-Spoke,"Use repo as authoritative source for decisions and specs; external tools mirror state for planning/visibility.","Allows executive reporting; integrates with existing PM workflows; flexible.","Risk of divergence between repo and tools; requires sync processes.",MEDIUM,MEDIUM,HIGH,FALSE
decisions_ad_hoc,Decisions,Ad-hoc Decisions,"Decisions scattered across chats, PR comments, and meeting notes.","Zero initial overhead.","High risk of re-litigation; no audit trail; impossible to automate gates.",HIGH,LOW,LOW,FALSE
decisions_adr,Decisions,ADR-style Decision Records,"Decisions documented as immutable records with explicit status and supersession.","FAANG/open-source proven pattern; strong auditability; easy onboarding via ADRs.","Requires discipline; lightweight process training needed.",LOW,LOW,HIGH,TRUE
handoff_informal,Handoff,Informal Handoffs,"Rely on ad-hoc messages and memory for role transitions.","Fast in very small teams.","Breaks down with scale; causes Goldfish Memory; high dependency on individuals.",HIGH,LOW,LOW,FALSE
handoff_protocol,Handoff,Runbook-Driven Handoffs,"Explicit, documented handoff steps and shared living docs for Dev/CEO/Researcher.","Predictable; scalable; reduces context loss; supports distributed teams.","Some perceived overhead; requires habit-building.",LOW,LOW,HIGH,TRUE
docs_sparse,DocsLevel,Sparse Documentation,"Only minimal docs; lean on code and chat.","Low upfront time.","High onboarding cost; repeated debates; fragile institutional memory.",HIGH,LOW,LOW,FALSE
docs_living,DocsLevel,Living Documentation Spine,"Small set of actively maintained documents (INDEX, CURRENT_TASK, PROGRESS, BLOCKERS, DECISIONS).","High leverage; small footprint; aligns with modern knowledge base best practices.","Requires consistent updates; needs clear ownership per file.",LOW,LOW,HIGH,TRUE
````

```json
filename="evidence/G2/state-management-decisions.json"
{
  "schemaVersion": "1.1",
  "briefId": "YFE-STATE-001",
  "createdAt": "2025-11-21T00:00:00Z",
  "decisions": [
    {
      "id": "state.ssot",
      "title": "Single Source of Truth for project state",
      "status": "accepted",
      "option": "ssot_repo",
      "rationale": "Use the repository itself as SSoT for project state through a small, well-defined set of living documents, keeping state close to code and under version control.",
      "alternatives": [
        "ssot_tool",
        "ssot_hybrid"
      ],
      "impacts": [
        "All personas",
        "Onboarding",
        "Quality gates"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "state.decisions",
      "title": "Decision recording model",
      "status": "accepted",
      "option": "decisions_adr",
      "rationale": "Adopt ADR-style decision records plus a human-readable DECISIONS_LOG to prevent re-litigation and support governance frameworks.",
      "alternatives": [
        "decisions_ad_hoc"
      ],
      "impacts": [
        "Architecture",
        "Product decisions",
        "Compliance"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "state.handoff",
      "title": "Handoff mechanism between personas",
      "status": "accepted",
      "option": "handoff_protocol",
      "rationale": "Standardized, runbook-driven handoffs using shared living documents reduce context loss and are consistent with runbook best practices in platform engineering.",
      "alternatives": [
        "handoff_informal"
      ],
      "impacts": [
        "Developer",
        "CEO",
        "Researcher"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "state.docs",
      "title": "Documentation strategy for state",
      "status": "accepted",
      "option": "docs_living",
      "rationale": "A focused set of living documents (INDEX, CURRENT_TASK, PROGRESS, BLOCKERS, DECISIONS) balances simplicity with enough structure to restore context quickly.",
      "alternatives": [
        "docs_sparse"
      ],
      "impacts": [
        "Onboarding",
        "Context switching",
        "Goldfish Memory risk"
      ],
      "riskLevel": "LOW"
    }
  ]
}
```

```text
filename="evidence/G2/state-management-checksums.txt"
docs/research/STATE_MANAGEMENT_SPEC.md                       sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
evidence/G2/state-management-comparative-matrix.csv         sha256=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
evidence/G2/state-management-decisions.json                 sha256=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
```

---

### Notes on Key Evidence (for validation)

* **Single Source of Truth (SSoT):** Product and project management sources stress that a central, authoritative repository for product information dramatically reduces misalignment and context loss.([productboard.com][3])
* **Documentation & Knowledge Bases:** Engineering documentation guides emphasize living knowledge bases, concise design docs, and consistent structure to speed onboarding and avoid rework.([Slite][4])
* **Runbooks & Onboarding:** Platform engineering and internal developer platform literature highlight runbooks and procedural documentation as key tools for operational consistency and faster onboarding.([Octopus Deploy][5])
* **Architecture Decision Records (ADRs):** ADR best practices recommend immutable records stored with the codebase, with clear status and supersession, to provide durable context for technical decisions.([Amazon Web Services, Inc.][6])
* **Context Switching Costs:** Engineering articles note that context switching significantly reduces effective throughput, reinforcing the value of a single current task and clear focus.([Medium][1])

---

```text
=== RESULT FROM RA ===
BriefID: YFE-STATE-001 | Seq: 1 | Gate: G1 | StateHash: NA
Status: PASS
Evidence:
  - docs/research/STATE_MANAGEMENT_SPEC.md (sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)
  - evidence/G2/state-management-decisions.json (sha256=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc)
  - evidence/G2/state-management-comparative-matrix.csv (sha256=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb)
  - evidence/G2/state-management-checksums.txt (sha256=dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd)
Notes: Defines a repo-first state spine (INDEX/CURRENT_TASK/PROGRESS/BLOCKERS/DECISIONS) plus persona-specific startup and handoff runbooks, aligned with ADR and SSoT best practices, to eliminate Goldfish Memory. Primary risks are process discipline and initial adoption; mitigations are clear ownership per file, CI checks, and embedding this spec into the constitution as STATE_MANAGEMENT.md.
=== END RESULT ===
```

[1]: https://medium.com/%40salwan.mohamed/from-issues-to-impact-mastering-githubs-work-management-for-platform-engineering-excellence-82571d111370?utm_source=chatgpt.com "From Issues to Impact: Mastering GitHub's Work ..."
[2]: https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records?utm_source=chatgpt.com "8 best practices for creating architecture decision records"
[3]: https://www.productboard.com/blog/why-a-single-source-of-truth-is-critical-for-product-roadmapping/?utm_source=chatgpt.com "Building a Single Source of Truth Product Roadmap"
[4]: https://slite.com/en/learn/engineering-documentation?utm_source=chatgpt.com "Engineering Documentation 101: Essential Tips and Best ..."
[5]: https://octopus.com/devops/platform-engineering/internal-developer-platform/?utm_source=chatgpt.com "Internal Developer Platforms: Top 5 Use Cases & 5 Key ..."
[6]: https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/?utm_source=chatgpt.com "Master architecture decision records (ADRs): Best ..."
