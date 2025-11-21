````markdown
<!-- docs/research/ROADMAP_SPEC.md -->

# ROADMAP SPECIFICATION – “YOUR FIRST ENGINEER”

## Executive Summary

This document defines the product mission, target user, competitive positioning, and phased roadmap for “Your First Engineer” (YFE), an autonomous AI system that turns plain-language ideas into production-ready applications. The goal is to combine the speed of modern AI app builders with FAANG-grade reliability, quality gates, and a transparent build story.

We target non-technical and “semi-technical” founders who today rely on tools like v0, Bolt, Replit Agent, and Cursor to prototype in minutes or weekends, but still struggle to reach auditable production quality without hiring engineers. The roadmap is organized into six phases (P0–P5), each with explicit objectives, success criteria, deliverables, dependencies, validation flows, timelines, and risks. Phases are ordered to first establish guardrails (architecture, quality gates, state management), then ship the Production Toggle MVP, then layer on AI Test Users, Build Story, multi-tenant scale, and finally fully autonomous engineering mode.

---

## 1. Product Goal & Positioning (RQ1)

### 1.1 Mission Statement (One Sentence)

Your First Engineer turns a non-technical founder’s plain-language idea into a **deployed, test-covered, auditable production web app** in under an hour, using an AI “first hire” that works through a governed engineering pipeline instead of ad-hoc magic.

### 1.2 Target User Persona

**Decision-maker:** Solo or small-team founder (non- or semi-technical), typically:

- Background: Domain expert (e.g., ops, marketing, consulting, healthcare, education) with limited coding depth.
- Stage: Pre-seed to Series A; needs to validate 1–3 SaaS ideas quickly.
- Constraints:
  - Cash-constrained: cannot afford a full-time senior engineer.
  - Time-constrained: needs working software (not just prototypes) in days/weeks.
  - Risk-averse: afraid of “agent deletes production DB”-style incidents and opaque AI behavior.

**Pain Points Today**

- Tools like v0, Bolt, and Lovable let them go from idea to prototype UI or full app in minutes to a weekend, but:
  - They lack **stable, repeatable production criteria** (tests, monitoring, rollbacks).
  - They still need human engineers to wire complex backends, harden security, and clean up code.
  - They get **no auditable build story** (what changed, why, and what was tested).
- Agent tools (Replit Agent 3, Cursor Composer) show impressive autonomy and self-testing, but:
  - Are optimized for developers working in IDEs.
  - Have had high-profile failure modes when given too much power without guardrails.

### 1.3 Measurable Success Criteria

By the end of Phase 3 (Build Story):

1. **Time-to-Production**
   - For a standard starter use case (CRUD SaaS with auth, basic dashboard), a non-technical founder can:
     - Go from natural-language description to deployed HTTPS web app with a production toggle, seed data, and one core flow fully tested **in ≤60 minutes**, using only a browser and the Owner Console.
   - 80% of such attempts succeed without manual code edits.

2. **Quality & Safety**
   - All generated apps meet minimum standards:
     - **Code quality:** Lint-clean (no errors, no warnings) for both frontend and backend.
     - **Testing:** ≥80% line coverage on new or modified backend code; ≥70% on new frontend logic; project-wide baseline ≥60% coverage with a plan to raise thresholds over time.
     - **Incidents:** ≤1 P1 incident per 20 production toggles in the first 30 days, with automatic rollback paths and a captured post-incident build story.

3. **Operator Experience (Owner + CEO)**
   - 90% of operations (new build, rollback, inspecting build story, reviewing AI test sessions) can be done:
     - From the browser, in the Owner/CEO consoles.
     - Without reading raw code, logs, or touching the CLI.
   - Each build exposes a **single “Build Story” page** summarizing:
     - Requirements, architecture decisions, diffs, tests, AI user runs, and approvals.

### 1.4 Competitive Landscape & Positioning

#### v0 (Vercel)

- **What it does well:**  
  - “Generate UI with AI… deploy to production in seconds.”  
  - Turns natural language into production-ready frontend components and can sync output to GitHub.  
- **Limitations for our use case:**
  - Optimized for UI and component generation; backend logic, data modeling, and long-horizon build stories remain manual or external.
  - Production readiness (tests, monitoring, rollbacks) is largely left to the developer and the broader Vercel ecosystem.
- **Implication for YFE:**  
  - We must **own the full stack (frontend + backend + infra)** and add a governed pipeline, not just UI generation.

#### Bolt.new (StackBlitz)

- **What it does well:**
  - In-browser IDE with AI; users report building full-stack apps in minutes to hours, including Stripe/Supabase integrations, without local setup.
  - Strong “vibe coding” stories: novices building e-commerce sites in ~6 hours, and “built in a weekend” product case studies.
- **Limitations for our use case:**
  - Focus is on rapid building and deployment; production checks (tests, gating, safety) are less opinionated and depend on the human operator.
- **Implication for YFE:**
  - YFE should match Bolt’s **time-to-first-app** while adding:
    - Automated synthetic QA.
    - Hard production gates.
    - A non-technical Owner Console with plain-English validation flows.

#### Replit Agent 3

- **What it does well:**
  - Highly autonomous agent that builds, tests (via browser), fixes code, and can generate new agents and workflows.
  - Reflection loops and proprietary app testing emphasize **self-testing and self-repair.**
- **Known risk:**
  - Real-world incident where an AI agent deleted a production database and then misrepresented its actions, despite “freeze” instructions, highlighting the danger of unrestricted autonomy.
- **Implication for YFE:**
  - We must **separate “sandbox build” from “production toggle”** with:
    - Strong human-in-the-loop approvals.
    - Fine-grained permissions and isolation.
    - Verifiable logs / build stories before any production change.

#### Cursor Composer

- **What it does well:**
  - Low-latency agentic coding inside the editor; most turns complete under 30s.
  - Supports multi-agent workflows and codebase-wide semantic search; optimized for professional engineers.
- **Limitations for our use case:**
  - Requires an IDE and baseline engineering skill.
  - Focus is on **augmenting engineers**, not replacing the first engineering hire for non-technical founders.
- **Implication for YFE:**
  - Position YFE as: **“Your first autonomous hire”** vs. Cursor as “your power tool once you have engineers.”  
  - We trade some raw flexibility for **governed, auditable flows and a stable stack.**

#### Positioning Summary

- **North Star:** “From idea → production-ready app with a defensible build story, not just a flashy demo.”
- **Differentiators:**
  - Opinionated stack & architecture (Next.js + LangGraph).
  - Strong state management and quality gates (G1–G11).
  - Built-in **Production Toggle**, synthetic AI test users, and Build Story as first-class features.
  - Designed first for **non-technical operators**, while remaining acceptable to senior engineers.

---

## 2. Roadmap Overview

### 2.1 Phase List

| Phase | Name                             | Core Capability Unlocked                                                   |
|-------|----------------------------------|----------------------------------------------------------------------------|
| P0    | Foundations & Guardrails        | Architecture, state management, quality gates, and execution protocol      |
| P1    | Production Toggle MVP           | Single-project flow from idea → sandbox app → gated production toggle      |
| P2    | Synthetic User QA               | AI test users that probe, regress, and gate deployments                    |
| P3    | Build Story & Replay            | End-to-end build story (decisions, diffs, tests, runs) & replay UI         |
| P4    | Multi-Project & Multi-Tenant    | Multiple owners, projects, sandboxes; resource isolation & scaling         |
| P5    | Autonomous Engineering Mode     | Backlog management, continuous improvement, and limited self-initiated work|

### 2.2 Roadmap Diagram (Mermaid)

```mermaid
graph TD
  P0["P0: Foundations & Guardrails"] --> P1["P1: Production Toggle MVP"]
  P1 --> P2["P2: Synthetic User QA"]
  P2 --> P3["P3: Build Story & Replay"]
  P3 --> P4["P4: Multi-Project & Multi-Tenant"]
  P4 --> P5["P5: Autonomous Engineering Mode"]
````

---

## 3. Detailed Phases (RQ2)

For each phase:

* **Objective** – What capability is unlocked.
* **Success Criteria** – How we know it works.
* **Deliverables** – Concrete artifacts/features.
* **Dependencies** – What must be ready.
* **Owner Validation (≤20 min, browser-only)** – How the Owner checks it.
* **Timeline (Evidence-based estimate)** – With justification.
* **Risks & Mitigations** – Top 1–2.

### Phase 0: Foundations & Guardrails

**Objective**
Create a hardened foundation so every later phase is “production from line 1”: architecture, state management, execution framework, and quality gates G1–G11.

**Success Criteria**

1. `COMPLETE_ARCHITECTURE_SPEC.md`, `STATE_MANAGEMENT_SPEC.md`, `ROADMAP_SPEC.md`, `EXECUTION_PROTOCOL_SPEC.md`, and `NOVEMBER_2025_STANDARDS.md` are complete, approved, and versioned.
2. Repository structure, tooling, and CI scaffold exist:

   * Monorepo with apps, packages, and LangGraph service.
   * Baseline CI pipeline that runs lint, tests, and coverage for “hello world” flows.
3. Evidence directories (`evidence/G1`…`G11`) and templates exist and are enforced by CI.

**Deliverables**

* Monorepo with:

  * `apps/owner-console`, `apps/agent-console` (if separate), `services/agent-runtime` (LangGraph 1.0.3), `services/sandbox-host`.
* CI/CD pipeline skeleton with:

  * Lint + tests + coverage for both Python and TypeScript.
  * Evidence upload/file checks for at least G1–G5.
* Initial **state management** implementation:

  * Persona startup checklists.
  * `task.md`, `progress.md`, `blockers.md` conventions.
  * Session log format.
* Developer/CEO/Researcher execution templates.

**Dependencies**

* None (starting phase), but must align with:

  * VISION (Production Toggle, AI Test Users, Build Story).
  * CLAUDE quality gates (G1–G11) – we assume mapping but must reconcile names.

**Owner Validation (≤20 min)**

1. Open Owner Console in browser.
2. Run “System Self-Check” task that:

   * Executes a dummy build pipeline.
   * Produces a minimal app artifact.
   * Outputs evidence links under `evidence/G1–G5`.
3. Confirm:

   * All checkboxes in a **Phase 0 Completion Checklist** page are green.
   * A sample task’s build story is captured (even if trivial).

**Timeline (2–3 weeks)**

* Reference MVP timelines: simple but robust SaaS MVPs commonly take **4–8 weeks** end-to-end; foundational infra typically consumes 25–40% of that time in well-run teams.
* With a narrow stack and no end-user features, 2–3 weeks for a small, focused team is realistic.

**Risks & Mitigations**

* **Risk (MED):** Over-designing architecture before seeing real workloads.
  **Mitigation:** Keep P0 scope strictly to what later phases require; postpone scaling and multi-tenant concerns to P4.
* **Risk (MED):** CI/evidence complexity slows iteration.
  **Mitigation:** Start with a minimal but strict subset of gates (G1–G5) in P0 and extend in later phases.

---

### Phase 1: Production Toggle MVP

**Objective**
Deliver the first vertical slice where a non-technical owner can describe an app, have YFE generate and run it in a sandbox, and then **explicitly toggle** a gated “Promote to Production” action.

**Success Criteria**

1. From Owner Console:

   * Owner enters idea (e.g., “Client CRM with contacts, notes, and simple funnel.”).
   * System:

     * Generates requirements/spec.
     * Proposes architecture.
     * Builds app and deploys to a sandbox URL.
2. Owner can:

   * Explore app in sandbox.
   * View basic test results (unit/smoke tests).
   * Inspect a minimal build story (what was built, which tests ran).
3. Production Toggle:

   * Disabled until:

     * Lint is clean.
     * Tests pass.
     * Coverage thresholds for new code are met.
   * When toggled:

     * A production deployment is created in an isolated environment.
     * A signed build story snapshot and evidence bundle are stored.

**Deliverables**

* **Owner Console v1**

  * Prompt input, spec view, build progress stream (LangGraph events -> frontend).
  * Sandbox URL and Production URL surfaces.
  * “Production toggle” with precondition indicators.
* **Agent Runtime**

  * LangGraph 1.0.3 graph implementing a basic Engineer → Reviewer chain with interruptions for approvals.
  * Postgres or similar checkpointer for graph state.
* **Sandbox Infrastructure**

  * Per-app ephemeral environment (e.g., containers or serverless functions) with clear teardown policy.
  * No direct production access from LangGraph without passing through gating service.
* **Evidence Integration**

  * Evidence bundle for each build (tests, logs, diffs) automatically collected into `evidence/` by CI/agent runtime.

**Dependencies**

* P0 Foundations completed and stable (repo, CI, evidence).
* At least one starter template (e.g., Next.js + FastAPI) fully wired.

**Owner Validation (≤20 min)**

1. Create one sample app from scratch.
2. Confirm:

   * Sandbox app runs (basic CRUD works).
   * test summary visible in UI.
   * “Production Toggle” initially disabled; shows unmet checks (e.g., coverage).
3. Press Production Toggle once it becomes enabled:

   * Confirm production URL and evidence link work.
   * Confirm build story exists and includes at least requirements, architecture, and test summary.

**Timeline (3–5 weeks)**

* Building a thin vertical slice UI + LangGraph + infra is comparable to a small SaaS MVP feature set.
* Industry data suggests simple MVPs can be delivered in **4–8 weeks**; with P0 foundations already done, 3–5 weeks for P1 is reasonable.

**Risks & Mitigations**

* **Risk (HIGH):** Production toggle misconfigured, enabling unsafe deploys.
  **Mitigation:** Treat production toggle as its own service with strict checks and explicit approvals; implement “dry-run” mode initially.
* **Risk (MED):** Over-scope initial app templates.
  **Mitigation:** Start with one canonical vertical (e.g., simple CRM) and extract patterns later.

---

### Phase 2: Synthetic User QA (AI Test Users)

**Objective**
Introduce AI test users that exercise generated apps in sandbox and production-like environments, producing structured test and UX feedback that gates production.

**Success Criteria**

1. For each new build:

   * Synthetic users execute at least:

     * One happy-path flow.
     * One error-path flow.
   * They produce:

     * Click-level trace.
     * Screenshots or state snapshots.
     * Structured bug reports (if failures).
2. Production toggle requires:

   * All synthetic tests pass OR
   * Known issues accepted with explicit waivers by CEO/Owner.
3. Build story includes a **“Synthetic QA”** section:

   * Test cases.
   * Outcomes.
   * Links to replays/screenshots.

**Deliverables**

* **Synthetic User Engine**

  * LangGraph nodes that:

    * Spin up browser sessions (e.g., via Playwright or similar, per architecture spec).
    * Interpret requirements into test plans.
    * Interact with the app like a user (clicks, form submissions).
  * Storage for test artifacts (videos, screenshots).
* **QA Console (sub-view of Owner/CEO console)**

  * Visual timeline of synthetic user journeys.
  * Simple pass/fail and error categorization.
* **Gates**

  * New quality gate (e.g., G6) for synthetic QA:

    * Fails builds if core journeys fail.
    * Allows waivers but requires documented justification.

**Dependencies**

* P1: Production Toggle MVP must be fully working.
* Browser automation stack and sandbox environment must be stable.

**Owner Validation (≤20 min)**

1. Trigger a new build.
2. Observe synthetic QA runs:

   * Confirm at least one success path and one intentional failure (e.g., invalid form).
3. Open QA view:

   * Review screenshot or replay.
   * See how failure blocked production toggle until resolved or explicitly waived.

**Timeline (4–6 weeks)**

* Building robust synthetic test systems with browser automation typically takes several weeks; using modern tooling (Playwright, Vitest’s browser mode, etc.) and leveraging patterns from tools like Replit Agent 3 and modern testing frameworks, 4–6 weeks is a realistic target for a focused team.

**Risks & Mitigations**

* **Risk (HIGH):** Flaky synthetic tests block builds or erode trust.
  **Mitigation:**

  * Start with a small, stable set of tasks (login, main flow).
  * Track flakiness separately and require manual approval for flaky tests.
* **Risk (MED):** Synthetic users miss critical edge cases.
  **Mitigation:** Allow Owner/CEO to define additional “critical paths” in plain language that are turned into tests.

---

### Phase 3: Build Story & Replay

**Objective**
Provide an end-to-end, human-readable build story for each app and deployment—capturing decisions, diffs, tests, synthetic QA, approvals, and incidents—so CEOs and Owners can audit work without reading code.

**Success Criteria**

1. Every production deployment has a **Build Story** document capturing:

   * High-level requirements and scope.
   * Architectural decisions (stack, services, data model changes).
   * Code diffs summary (not raw diff dumps).
   * Testing summary (unit, integration, coverage, synthetic QA).
   * Approvals and waivers.
   * Any post-deploy incidents and rollbacks.
2. Build story is accessible:

   * From Owner and CEO consoles with a single click.
   * As an exportable artifact (PDF/Markdown) for audits.

**Deliverables**

* **Build Story Engine**

  * LangGraph nodes that collate and summarize:

    * Task.md, progress.md, blockers.md.
    * CI outputs, coverage reports, synthetic QA logs.
  * Storage schema for build story snapshots.
* **UI**

  * Build Story page with:

    * Timeline of key events.
    * Links to evidence files.
    * Plain-English narrative generated from LangGraph with guardrails.
* **Incident Tracking**

  * Simple incident records linked to builds.
  * Post-incident build story updates.

**Dependencies**

* P1 & P2 complete and stable; all key evidence already collected for each build.

**Owner Validation (≤20 min)**

1. Pick a completed build.
2. Open Build Story page.
3. Confirm it answers, in plain language:

   * What was built?
   * What changed from previous version?
   * Which tests ran and passed/failed?
   * Who/what approved it and why?
4. Export Build Story and verify includes evidence links.

**Timeline (3–4 weeks)**

* Summarization and narrative generation are well-served by current state-of-the-art LLMs; the main effort is **schema design and integration**, which is similar in complexity to implementing an internal audit log and reporting feature.

**Risks & Mitigations**

* **Risk (MED):** Build story becomes too long or noisy.
  **Mitigation:** Provide layered detail (high-level summary first, drill-down sections).
* **Risk (MED):** Narrative misrepresents facts (e.g., test status).
  **Mitigation:** Generate narrative strictly from structured data; never allow the model to “guess” a result that isn’t present.

---

### Phase 4: Multi-Project & Multi-Tenant Scale

**Objective**
Scale YFE to multiple owners, projects, and concurrent builds with strong isolation and resource controls, while keeping the same guarded production model.

**Success Criteria**

1. Multiple Owner accounts and projects are supported:

   * Clear per-project build stories, evidence, and environment separation.
2. Sandboxes and production environments are:

   * Isolated per project/owner (no cross-contamination).
   * Auto-cleaned for stale sandboxes.
3. System handles:

   * At least N concurrent builds (set initial target, e.g., 10–20) with acceptable latency.

**Deliverables**

* **Multi-tenant data model**

  * Owners, projects, environments, builds, and users.
* **Resource manager**

  * Controls sandbox creation, teardown, and quotas.
* **Security**

  * Strict separation of evidence, logs, and configs across tenants.

**Dependencies**

* P1–P3 fully working for single-tenant.
* State management and execution protocols are stable.

**Owner Validation (≤20 min)**

1. Create a second project under same Owner.
2. Trigger builds for both.
3. Confirm:

   * Separate sandboxes and production URLs.
   * Separate build stories and evidence paths.
   * No cross-project leakage.

**Timeline (4–6 weeks)**

* Multi-tenant hardening is a classic step for SaaS platforms and often consumes several weeks; the complexity is in permissions, data isolation, and infra scaling rather than net-new features.

**Risks & Mitigations**

* **Risk (HIGH):** Cross-tenant data or infra leakage.
  **Mitigation:**

  * Use per-tenant namespaces and strong authz models.
  * Add targeted tests and PRRs focusing on multi-tenant isolation.
* **Risk (MED):** Cost blow-ups due to too many sandboxes.
  **Mitigation:** Quotas, TTLs on sandboxes, and cost dashboards.

---

### Phase 5: Autonomous Engineering Mode

**Objective**
Enable YFE to operate as a semi-autonomous engineering partner: managing backlogs, proposing experiments, and executing changes within strict guardrails and quality gates.

**Success Criteria**

1. Owners can define:

   * A backlog of tasks.
   * Policies (e.g., “No breaking changes after 18:00,” coverage thresholds, change windows).
2. YFE can:

   * Propose new tasks (e.g., performance optimizations, refactors) with evidence-backed justifications.
   * Execute tasks automatically within agreed limits (e.g., only in sandbox or can auto-promote low-risk changes).
3. All actions still pass through:

   * Quality gates G1–G11.
   * Build story and evidence capture.

**Deliverables**

* **Backlog & Policy Engine**

  * Plain-English configurations for risk thresholds and windows.
* **Autonomous Mode**

  * LangGraph flows that:

    * Periodically inspect metrics and code health.
    * Schedule maintenance tasks.
    * Execute them under the same gated pipeline.
* **Safety**

  * Kill switches and easy rollback.
  * Monitoring plus anomaly detection for unusual behavior.

**Dependencies**

* All previous phases complete and hardened.
* Observability and metrics feeding into decisions.

**Owner Validation (≤20 min)**

1. Turn on Autonomous Mode for one low-risk project with tight constraints (sandbox-only).
2. Review:

   * Tasks proposed and executed autonomously.
   * Build stories generated for autonomous work.
3. Confirm:

   * Manual override works (pause, rollback).
   * No production change occurs without explicit Owner/CEO policies allowing it.

**Timeline (6–10+ weeks)**

* Autonomous mode is a compound feature: combining backlog management, risk evaluation, and safe agent autonomy.
* Timeline depends heavily on learnings from P1–P4; starting with limited-scope autonomy (maintenance & refactoring) will likely be the safest approach.

**Risks & Mitigations**

* **Risk (HIGH):** Autonomous changes cause regressions or incidents.
  **Mitigation:**

  * Start sandbox-only.
  * Require human approvals for any production toggles.
  * Use strict coverage, QA, and incident thresholds.
* **Risk (HIGH):** Regulatory alignment (e.g., EU AI Act) as “high-risk” system.
  **Mitigation:**

  * Design with logging, transparency, and human oversight from the start.
  * Maintain traceable logs and build stories per deployment.

---

## 4. Roadmap to Validation

For each phase, we commit to:

* **Entry Criteria:** Previous phases’ success criteria met and signed off with evidence.
* **Exit Criteria:** All phase-specific success criteria met; evidence stored under appropriate `evidence/G*` folders; at least one end-to-end example completed and documented.
* **Review:** CEO + Owner review Build Story for at least one canonical build before moving to the next phase.

````

---

### Source Notes (Key Evidence Used)

- Competitors deliver “idea to app in minutes/hours,” indicating feasibility of YFE’s time-to-production targets: v0, Bolt, and similar AI app builders emphasize going from prompt to functional UI or app rapidly, often **in minutes** for prototypes and a **weekend** for full products.   
- Replit Agent 3 demonstrates autonomous build/test/fix loops and browser-based self-testing, but also suffered a catastrophic incident where an AI agent deleted a production database and misrepresented its actions, underscoring the need for strong guardrails. :contentReference[oaicite:1]{index=1}  
- Cursor’s Composer model shows that **low-latency agentic coding** (turns <30s) is now standard for high-end coding agents, supporting our roadmap’s assumption that multi-step AI flows can be user-acceptable if properly governed.   
- Industry data on MVP timelines suggests 4–8 weeks is a common benchmark for simple MVPs, with 8–16 weeks for more complex products, supporting phase time estimates when combined with agentic acceleration.   
- Production readiness and operational excellence frameworks (AWS Well-Architected, Google SRE’s Production Readiness Review) emphasize structured checklists, reliability gates, and ongoing readiness rather than one-off launches—this informs the gated, evidence-driven nature of each phase. :contentReference[oaicite:4]{index=4}  

---

```markdown
<!-- docs/research/EXECUTION_PROTOCOL_SPEC.md -->

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

---

### Source Notes (Key Evidence Used)

- Production readiness and operational excellence frameworks stress documented checklists, repeatable processes, and evidence-backed reviews (e.g., Google SRE’s Production Readiness Review, AWS Well-Architected, and modern production readiness checklists). :contentReference[oaicite:5]{index=5}  
- Modern code review and PR checklist tooling (e.g., GitHub PR templates, “pull checklist” apps) show the value of structured, enforced checklists linked to merge gates—YFE’s evidence and gate structure generalizes this pattern.   
- “Operations as code” and “everything as code” principles from AWS Well-Architected and related commentary support the idea of representing tasks, gates, and evidence as versioned artifacts in the repo. :contentReference[oaicite:7]{index=7}  

---

```markdown
<!-- docs/research/NOVEMBER_2025_STANDARDS.md -->

# NOVEMBER 2025 STANDARDS SPECIFICATION

## Executive Summary

This document pins tool versions and defines quantitative thresholds for each quality gate (G1–G11) as of November 21, 2025. It aligns with mainstream 2025 practices for code quality, testing, security, and AI risk, drawing on guidance from large engineering organizations, testing vendors, and standards bodies. Where the existing constitution defines named gates in CLAUDE.md, this document provides **concrete, evidence-backed standards** that can be mapped to those gates.

The core stance is: **new code must be lint-clean, type-checked, and well-tested (≥80% coverage) with clear production readiness and AI-specific safety practices.** These standards are enforced via CI checks and evidence artifacts under `evidence/G*/`. Tool versions are pinned to late-2025 stable releases (no alphas) to balance stability and currency.

---

## 1. Scope & Mapping

We define 11 gates:

1. G1 – Research & Problem Definition  
2. G2 – Architecture & Design  
3. G3 – Security & Compliance  
4. G4 – Code Quality (Style, Lint, Types)  
5. G5 – Testing & Coverage  
6. G6 – Synthetic QA (AI Test Users)  
7. G7 – Observability & Reliability  
8. G8 – Data, Privacy & Governance  
9. G9 – AI Risk & Safety (including EU AI Act readiness)  
10. G10 – UX, Accessibility & Product Fit  
11. G11 – Operational Readiness & Launch

If CLAUDE.md uses different names or ordering, map each gate to these categories but **keep the standards and thresholds intact.**

---

## 2. Global Tooling Baseline (Pinned Versions)

### 2.1 JavaScript / TypeScript

- **Node.js:**  
  - Use latest active LTS in late 2025 (Node 22 LTS) as default runtime for tooling and Next.js.  
- **ESLint:**  
  - Use `eslint` **9.39.x** (latest stable line as of early November 2025).  
  - Do **not** adopt ESLint 10 alpha in production; alpha releases introduce breaking changes and are not considered stable.
- **Test Frameworks:**
  - **Jest 30.2.x** for legacy/Node-centric tests:
    - Jest 30 (2025) focuses on real-world performance improvements and memory/jest resolution enhancements.
  - **Vitest 4.0.x** for Vite/Next-aligned projects:
    - Vitest 4 (October 2025) offers browser mode, visual regression support, and an improved coverage pipeline.
  - Choose **one primary** (Vitest for new frontends; Jest for Node-heavy code) to minimize complexity.

### 2.2 Python

- **Runtime:**  
  - Python **3.11** minimum; prepare for 3.12 once all key tools fully support it.
- **Linters/Formatters:**
  - **Ruff** as primary linter/formatter:
    - Modern, extremely fast; can replace much of Flake8, isort, and Black in one tool.
  - Optionally keep **Flake8 7.3.0** for legacy plugins:
    - Latest release June 2025.
- **Type Checker:**  
  - **mypy 1.18.x** (September 2025 line).
- **Testing & Coverage:**
  - **pytest 9.0.x** (latest stable November 2025).
  - **coverage.py 7.11–7.12.x**:
    - coverage 7.11/7.12 support modern Python versions and improved coverage capabilities.
  - Use `pytest-cov` to integrate coverage.py with pytest.

### 2.3 Shared & Security-Relevant Tools

- **Dependency & Supply-Chain**
  - Enforce lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, etc.) and pin versions, especially around known supply-chain incidents (e.g., compromised `eslint-config-prettier` and related npm packages in mid-2025).
- **Static Application Security Testing (SAST)**
  - Preferred: widely used SAST or code-scanning tools (e.g., GitHub Advanced Security, SonarQube, or similar) configured for JS/TS/Python.
- **CI/CD**
  - Use GitHub Actions or equivalent with:
    - Lint, type, test, coverage, SAST, and evidence existence checks per gate.

---

## 3. Gate Standards (G1–G11)

Each gate is defined by: purpose, tools, thresholds, automation.

### G1 – Research & Problem Definition

**Purpose**  
Ensure every significant task is grounded in up-to-date research, competitive analysis, or user insight—not guesswork.

**Artifacts**

- `evidence/G1/TASK-{TASK_ID}-research-report.md`  
  - Summary of problem, current alternatives, and references.
- `evidence/G1/TASK-{TASK_ID}-sources.json`  
  - JSON list of sources with URL, title, publisher, date, and short note.

**Standards**

- At least **3 independent, authoritative sources** (docs, research, reputable blogs, news).
- For market/tech claims, at least **1 primary source** (official doc or vendor).

**Automation**

- CI checks:
  - JSON is valid.
  - At least 3 entries in sources list.
- Manual CEO check:
  - Research summary aligns with cited sources.

---

### G2 – Architecture & Design

**Purpose**  
Ensure changes align with COMPLETE_ARCHITECTURE_SPEC and don’t introduce ad-hoc patterns.

**Artifacts**

- `evidence/G2/TASK-{TASK_ID}-design.md`
- `evidence/G2/TASK-{TASK_ID}-diagram.mmd` (Mermaid diagrams if needed).

**Standards**

- All non-trivial changes (new service, cross-boundary integration, data model change) require:
  - Description of alternatives considered and rationale for chosen approach.
  - Updated diagrams for non-local changes.

**Automation**

- CI:
  - For tasks marked with G2, fail if design evidence is missing.
- Manual:
  - CEO/Architect confirms alignment with architecture spec.

---

### G3 – Security & Compliance

**Purpose**  
Embed security into every change, aligned with NIST SSDF and CSF 2.0, and prepare for regimes like the EU AI Act.

**Artifacts**

- `evidence/G3/TASK-{TASK_ID}-threat-model.md`
- `evidence/G3/TASK-{TASK_ID}-sast-report.html`
- Additional SCA (Software Composition Analysis) reports where applicable.

**Standards**

- For features affecting auth, data storage, external APIs, or privileged operations:
  - Threat model with:
    - Assets, actors, entry points, and mitigations.
  - SAST run with:
    - 0 critical and 0 high-severity unresolved issues.
- Dependencies:
  - No known critical vulnerabilities in new/updated packages (per SCA).

**Automation**

- CI:
  - Run SAST and SCA on changed code.
  - Fail if critical/high issues remain untriaged.
- Manual:
  - CEO/security reviewer signs off threat model.

---

### G4 – Code Quality (Style, Lint, Types)

**Purpose**  
Ensure code is readable, consistent, and free of obvious smell/anti-pattern issues.

**Artifacts**

- `evidence/G4/TASK-{TASK_ID}-lint.txt`
- `evidence/G4/TASK-{TASK_ID}-types.txt`

**Tools & Versions**

- JS/TS:
  - `eslint` 9.39.x with project-specific config.
- Python:
  - `ruff` latest stable; optional `flake8` 7.3.x.
- Typing:
  - TS compiler and `mypy` 1.18.x for Python.

**Thresholds**

- Lint:
  - 0 errors, 0 warnings in CI.
- Types:
  - 0 type errors for files under test.
- Suppressions:
  - Any `eslint-disable`, `# noqa`, or `type: ignore` must be explicitly justified in TASK file.

**Automation**

- CI:
  - Run ESLint/Ruff/mypy; fail on any error/warning.
- Evidence:
  - Lint/type reports captured in evidence files.

---

### G5 – Testing & Coverage

**Purpose**  
Ensure robust automated tests with meaningful coverage.

**Artifacts**

- `evidence/G5/TASK-{TASK_ID}-pytest.txt`
- `evidence/G5/TASK-{TASK_ID}-frontend-tests.txt`
- `evidence/G5/TASK-{TASK_ID}-coverage-summary.txt`
- `evidence/G5/TASK-{TASK_ID}-coverage-html/` (directory or archive)

**Tools**

- Backend: `pytest` 9.0.x + `coverage.py` 7.11/7.12.
- Frontend: Jest 30.x or Vitest 4.x with integrated coverage.

**Coverage Thresholds**

- New/changed backend code:
  - **≥80% line coverage**, with branch coverage where practical.
- New/changed frontend logic:
  - **≥70% line coverage**.
- Overall project:
  - **≥60% line coverage** initially, with explicit plan to raise toward 80% as the product matures.

These values reflect widely cited recommendations where 80% is considered a good general target, with Google’s testing blog citing 60%/75%/90% as acceptable/commendable/exemplary ranges and multiple industry sources converging on ~70–80% as a practical, effective standard.

**Automation**

- CI:
  - Fail if coverage thresholds not met for new code or if overall coverage dips below baseline.
- Reports:
  - Coverage exports in machine-readable formats for dashboards.

---

### G6 – Synthetic QA (AI Test Users)

**Purpose**  
Catch end-to-end issues by having AI agents exercise the app in realistic flows (login, core features, error handling).

**Artifacts**

- `evidence/G6/TASK-{TASK_ID}-synthetic-runs.json`
- `evidence/G6/TASK-{TASK_ID}-synthetic-report.md`

**Standards**

- For every build with user-visible changes:
  - At least one **happy-path** scenario.
  - At least one **negative-path** scenario (invalid input/permissions).
- Synthetic tests must:
  - Pass without critical failures for core flows.
  - Be re-run after bug fixes affecting those flows.

**Automation**

- CI or post-deploy hooks automatically trigger synthetic runs in sandbox.
- Production toggle blocked if:
  - Synthetic QA fails on core flows and no waiver is provided.

---

### G7 – Observability & Reliability

**Purpose**  
Ensure each service is observable and meets basic reliability practices.

**Artifacts**

- `evidence/G7/TASK-{TASK_ID}-metrics-config.md`
- `evidence/G7/TASK-{TASK_ID}-alerts.md`
- Optional SLOs: `evidence/G7/TASK-{TASK_ID}-slos.md`

**Standards**

- New services/features must:
  - Emit logs with correlation IDs.
  - Expose at least:
    - One core request metric.
    - One error metric.
  - Have alerts on:
    - Error spikes.
    - Latency thresholds for key calls.

**Automation**

- CI lint checks for logging conventions.
- Deployment scripts validate observability configs present.

---

### G8 – Data, Privacy & Governance

**Purpose**  
Align with privacy expectations and prepare for compliance norms.

**Artifacts**

- `evidence/G8/TASK-{TASK_ID}-data-flow.md`
- `evidence/G8/TASK-{TASK_ID}-privacy-assessment.md`

**Standards**

- For any personal or sensitive data:
  - Document:
    - What fields are collected.
    - Where they are stored.
    - Retention and deletion policies.
  - Ensure:
    - Encryption in transit (TLS) and at rest (where relevant).
    - Access controls follow least privilege.

---

### G9 – AI Risk & Safety

**Purpose**  
Manage AI-specific risks in line with NIST AI RMF and the EU AI Act trajectory, even if YFE is not classified as “high-risk” initially.

**Artifacts**

- `evidence/G9/TASK-{TASK_ID}-ai-risk-assessment.md`
- `evidence/G9/TASK-{TASK_ID}-evals.md`

**Standards**

- For AI behaviors that:
  - Affect production deployments.
  - Interact with sensitive data.
  - Act autonomously over long horizons.
- The risk assessment must:
  - Identify misuse/failure scenarios (e.g., deleting data, pushing unsafe code).
  - Define human oversight and limits.
  - Capture logging and audit policies (minimum 6 months retention for high-impact actions).
- Evals:
  - For new autonomous behaviors, include targeted tests to probe:
    - Instruction following.
    - Safety constraints (e.g., cannot bypass production toggle).

---

### G10 – UX, Accessibility & Product Fit

**Purpose**  
Prevent obviously broken or inaccessible experiences.

**Artifacts**

- `evidence/G10/TASK-{TASK_ID}-ux-notes.md`
- `evidence/G10/TASK-{TASK_ID}-a11y-checklist.md`

**Standards**

- For new UI:
  - Basic accessibility checks (contrast, labels, focus).
  - Main flows work on desktop + mobile viewport sizes.
- Product fit:
  - At least one synthetic or human user run representing target persona.

---

### G11 – Operational Readiness & Launch

**Purpose**  
Ensure every change is launch-ready in the sense used by modern PRR (Production Readiness Review) practices: clear rollback, monitoring, documentation.

**Artifacts**

- `evidence/G11/TASK-{TASK_ID}-runbook.md`
- `evidence/G11/TASK-{TASK_ID}-prr-checklist.md`

**Standards**

- For any change that can impact production availability or behavior:
  - Runbook with:
    - How to deploy, monitor, rollback.
    - Known failure modes and mitigations.
  - PRR checklist completed:
    - Risk level.
    - Rollout plan.
    - Stakeholder approvals.

**Automation**

- CI checks presence of PRR evidence for tasks tagged as “launchable.”
- Releases blocked if G11 not satisfied.

---

## 4. Automation & CI Integration

- CI pipeline stages:
  - `g1_research_check` (evidence presence).
  - `g2_design_check` (evidence presence).
  - `lint`, `types`, `test`, `coverage` (G4–G5).
  - `sast`, `sca` (G3).
  - `synthetic_qa` (G6).
  - `observability_check` (G7).
  - `ai_risk_check` (G9 – for relevant tasks).
  - `prr_check` (G11 – for release branches).
- Any failing gate blocks merges and production toggles.

---

## 5. Review & Updates

- This standards document is re-validated **quarterly** against:
  - Tool release notes.
  - Industry guidance on coverage, security, and AI regulations.
- Changes are recorded in:
  - `NOVEMBER_2025_STANDARDS_CHANGELOG.md`
  - With tasks to adapt CI and evidence templates.

````

---

### Source Notes (Key Evidence Used)

* Tool versions and stability:

  * ESLint 9.39.x is the latest stable as of late October/early November 2025, with 10.x still in alpha; Jest 30.2.x is current stable; Vitest 4.0.x released in October 2025 with browser mode and visual regression; Flake8 7.3.0 released June 2025; mypy 1.18.1 released September 2025; coverage.py 7.11/7.12 released in late 2025; pytest 9.0.x released November 2025. ([eslint.org][1])
* Ruff is widely recognized as a modern, extremely fast Python linter/formatter, often replacing Flake8, isort, and Black. ([GitHub][2])
* Industry coverage guidance:

  * Google’s testing blog and subsequent summaries suggest 60% as acceptable, 75% commendable, 90% exemplary; Atlassian and multiple tool vendors commonly recommend ~80% as a good practical target. ([Google Testing Blog][3])
* Production readiness and PRR patterns:

  * Google SRE’s Launch Coordination Checklist and Production Readiness Review, GitLab’s production readiness review, and multiple modern checklists emphasize checklists, runbooks, risk assessment, and pre-launch reviews. ([sre.google][4])
* Security and AI risk frameworks:

  * NIST’s Secure Software Development Framework (SP 800-218) and its AI-specific community profile, NIST Cybersecurity Framework 2.0, and NIST AI Risk Management Framework 1.0 emphasize integrated security, risk-based controls, documentation, and AI-specific risk management; the EU AI Act and its early obligations stress logging, documentation, and human oversight for high-risk AI systems.
* Supply-chain risk:

  * 2025 incidents compromising npm packages like `eslint-config-prettier`, `eslint-plugin-prettier`, and utility libraries like `is` demonstrate the need for locked dependencies, SCA, and version pinning. ([TechRadar][5])

If you want, next step I can do is: (a) draft the `.template` folder contents (per-gate README + templates), or (b) adapt these gate standards to the exact G1–G11 names in your existing CLAUDE.md.

[1]: https://eslint.org/blog/2025/11/eslint-v10.0.0-alpha.0-released/?utm_source=chatgpt.com "ESLint v10.0.0-alpha.0 released"
[2]: https://github.com/astral-sh/ruff?utm_source=chatgpt.com "astral-sh/ruff: An extremely fast Python linter and code ..."
[3]: https://testing.googleblog.com/2020/08/code-coverage-best-practices.html?utm_source=chatgpt.com "Code Coverage Best Practices"
[4]: https://sre.google/sre-book/evolving-sre-engagement-model/?utm_source=chatgpt.com "Production Readiness Review: Engagement Insight"
[5]: https://www.techradar.com/pro/security/more-popular-npm-packages-hijacked-to-spread-malware?utm_source=chatgpt.com "More popular npm packages hijacked to spread malware"
