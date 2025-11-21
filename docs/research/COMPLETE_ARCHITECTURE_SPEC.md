````markdown
filename="docs/research/COMPLETE_ARCHITECTURE_SPEC.md"
# COMPLETE ARCHITECTURE SPEC – “YOUR FIRST ENGINEER”

File: docs/research/COMPLETE_ARCHITECTURE_SPEC.md  
Date: 2025-11-21  
BriefID: YFE-ARCH-001  

---

## 1. Scope & Objectives

**Goal.** Define a production-grade, LangGraph v1.0.3–native architecture for “Your First Engineer” (YFE), an autonomous system that turns plain-language ideas into production-ready applications, with:

- Clear stack and version choices (no ambiguity).
- A concrete, repo-level physical structure.
- A LangGraph design that can be implemented without extra clarification.

**Key constraints.**

- LangGraph **v1.0.3 (Python)**, Native `StateGraph` / `CompiledGraph`, and `astream_events(version="v2")` streaming.
- FAANG-grade non-functional requirements: reliability, observability, security, compliance alignment (ASVS 5.0, OWASP LLM Top 10 2025, NIST CSF 2.0, NIST SSDF SP 800-218, ISO/IEC 42001, EU AI Act).
- Architecture must be understandable and buildable by a new engineer with no prior context.

---

## 2. Stack & Versions

### 2.1 Frontend Framework – Next.js 15 vs 16

**Options.**

- **Next.js 15 (App Router)** – Stable release with React 19 support, updated caching defaults (uncached by default), and mature App Router.  
- **Next.js 16 (App Router)** – Adds stable React Compiler support, Turbopack as default bundler, improved caching APIs and routing/navigation, and requires Node.js ≥ 20.9.0 and TypeScript ≥ 5.1.0.

**Evidence (summarised).**

- Next.js 15 release: app router and caching changes; stable React 19 support.  
- Next.js 16: stable React Compiler, Turbopack default (2–5x faster builds), explicit caching APIs, enhanced routing, Node 20.9+ requirement.
- Real-world upgrade reports show mostly smooth migrations to 16 with some Turbopack edge cases in large monorepos, but dev/build performance gains once tuned.

**Trade-off summary.**

- **Stability:** 15 has had ~1 year of hardening; 16 is newer but built on the same App Router model and is now the primary supported line.
- **Performance & DX:** 16’s stable React Compiler + Turbopack and improved caching give better long-term performance and DX, especially for complex monorepos.
- **Longevity:** New work started in late 2025 should target 16 to avoid near-term major upgrades.

**Decision.** **Next.js 16 (App Router)** for Owner Console.

- **Version pin:** `next@16.0.x` (track 16.x with automated minor/patch updates via Renovate / Dependabot and a canary env).
- **Node.js runtime:** `node@20.9.x LTS` (minimum required by Next.js 16).
- **React:** `react@19.x`, `react-dom@19.x`.

---

### 2.2 CSS Framework – Tailwind CSS 3 vs 4

**Options.**

- **Tailwind 3.x**
  - Highly stable, widely adopted, JS-based `tailwind.config.js`.
  - Rich ecosystem of examples and templates.
- **Tailwind 4.0+**
  - CSS-first configuration, new engine, dedicated `@tailwindcss/cli` package.
  - Breaking changes vs 3 (config location, @tailwind directives, dark mode defaults, etc.).
  - Migration tools and official upgrade guide are available, but many reports of upgrade friction in existing projects.

**Context.**

- YFE is **greenfield**; we are not migrating a Tailwind 3 base.
- Tailwind 4 is the forward-looking line and already used in modern starters combining Next 15/16 + Tailwind 4 + shadcn/ui.

**Trade-off summary.**

- **Complexity:** Tailwind 4 adds initial cognitive load (CSS-based config) but simplifies long-term configuration.
- **Ecosystem:** Most new templates and guidance now assume Tailwind 4 for latest Next.js versions.
- **Risk:** Breaking changes are primarily migration-related; a greenfield project avoids most of this risk.

**Decision.** **Tailwind CSS 4.0+**.

- **Version pin:** `tailwindcss@4.0.x`, `@tailwindcss/cli@4.0.x`.
- Centralised theme tokens (colors, typography, spacing) will be treated as a product-level design system asset and owned by the Design / Frontend Platform sub-team.

---

### 2.3 UI Library – shadcn/ui

**Model.** shadcn/ui is a **code generator & design system** (CLI that copies components into the project), not a classic versioned library. Its current docs provide:

- Official Next.js integration, including React 19 support and monorepo mode.
- CLI support for monorepos (Turborepo/Nx) with explicit templates and guidance.

**Trade-off summary.**

- **Pros:**
  - Full control over component code; no runtime dependency lock-in.
  - Tailwind-native; good synergy with Tailwind 4.
  - Monorepo support via CLI, compatible templates and community guidance.
- **Cons:**
  - Responsibility for upgrades (regenerate components or manually sync with upstream).
  - Some monorepo setups (especially customised Turborepo/Nx) can hit rough edges that require manual fixups.

**Decision.** **shadcn/ui, CLI pinned + shared component package.**

- **CLI:** `shadcn@latest` at project start, then **pin to a specific version hash** in `package.json` after initial scaffolding.
- **Pattern:** Generate components into a shared `@yfe/ui` package in the monorepo so they can be reused by future apps (Owner Console, admin tools, marketing surfaces).
- **Policy:** No local per-app forks of components without an owning issue. All component changes go via `@yfe/ui`.

---

### 2.4 Backend Runtime – Python 3.11 vs 3.12+

**Options.**

1. **Python 3.11.x**
   - Very widely adopted in production; most AI and infra libraries test and publish wheels for 3.11 first.
   - LangGraph supports ≥ 3.11 and many auxiliary tools target 3.11 as default.
2. **Python 3.12.x**
   - Now broadly supported by core libraries (NumPy, Pandas, FastAPI, etc.) and considered mainstream.
   - Better performance vs 3.11 in many workloads.
3. **Python 3.13.x**
   - Stable since Oct 2024 with internal performance improvements.
   - LangGraph explicitly added compatibility for 3.13 and its CLI supports 3.11–3.13.
   - Ecosystem adoption still ramping; some packages lag behind.

**Evidence (summarised).**

- Python 3.13 released Oct 7, 2024; official docs describe it as a performance-focused major release.
- LangGraph changelog explicitly announces compatibility with Python 3.13 and LangGraph CLI supports Python ≥ 3.11 with explicit configuration for 3.11–3.13.
- Recent surveys show most production users still on 3.11 or 3.12, with 3.13 adoption < 20%, largely due to compatibility caution rather than blocking issues.

**Trade-off summary.**

- **3.11:** Safest library compatibility, but shorter remaining lifecycle horizon.
- **3.12:** Best balance between maturity and longevity; mainstream support, good performance, low risk.
- **3.13:** Most future-proof but slightly higher ecosystem risk.

**Decision.** **Python 3.12.x** for the Agent Runtime.

- **Version pin:** `python==3.12` (exact minor locked in infrastructure as code; allow micro bumps via security updates only).
- **Policy:** CI matrix includes 3.11 and 3.13 for LangGraph-heavy components so we can move up later with confidence.

---

### 2.5 Orchestration – LangGraph & Dependencies

**Mandate.** Use **LangGraph v1.0.3 (Python)** with Native graph APIs.

**Baseline packages (Python).**

- `langgraph==1.0.3` (or current 1.0.3 tag from PyPI) – durable agent runtime with `StateGraph`, `MessagesState`, checkpointers, streaming.
- `langchain-core==1.0.x` – core model abstractions compatible with LangGraph 1.0.
- `langgraph-checkpoint-postgres==3.0.x` – Postgres-based checkpoint saver recommended for production.
- `langchain-postgres==0.0.x` (if using `PostgresSaver` from this package instead of `langgraph-checkpoint-postgres`, depending on official guidance at implementation time).
- `pydantic>=2,<3` – model validation.
- `uvicorn` / `fastapi` (or `litestar`) – HTTP API & streaming transport layer for the Agent Runtime.

**Policy.**

- Respect LangGraph 1.x stability promise (no breaking changes until 2.0) by staying within **1.0.x** and regularly scanning release notes for security/bugfix updates.
- Pin exact versions via lockfiles (e.g., `uv` / `pip-tools`) and maintain a **staging environment** to test upgrades.

---

## 3. System Architecture

### 3.1 Repository Strategy – Monorepo vs Polyrepo

**Options.**

1. **Polyrepo**
   - Separate repos for Owner Console, Agent Runtime, Sandbox infra, shared libraries.
   - Pros: Clear operational isolation, simpler per-service CI.
   - Cons: Cross-repo changes are slower; shared UI and contracts drift easily.
2. **Monorepo with Turborepo (TypeScript + Python)**
   - Single repo containing:
     - `apps/web` (Owner Console),
     - `apps/agent-api` (Python service exposed via API gateway or direct),
     - `apps/sandbox-...`,
     - `packages/ui`, `packages/config`, `packages/contracts`, etc.
   - Pros: Easy atomic changes across frontend/backend contracts; great fit with Next.js 16 + shadcn monorepo support and Turborepo ecosystem.
   - Cons: Requires careful caching and task graph configuration; Turbopack still evolving.
3. **Monorepo with Nx**
   - Strong support for polyglot monorepos; good tooling and generators.
   - Slightly more friction with official Next.js/specific ecosystem tooling (compared to Turborepo).

**Decision.** **Monorepo with Turborepo.**

- Rationale: Best developer experience with Next.js 16 + shared UI + shared TypeScript contracts, and widely used with shadcn + Tailwind stacks. Python services can participate via custom `turbo` tasks for linting/tests, even though build tooling is separate.

---

### 3.2 High-Level Logical Architecture

**Services.**

1. **Owner Console (OC)** – Next.js 16 app
   - Responsibilities:
     - Project creation (“idea intake”), progress tracking, approvals (HITL), production toggle.
     - Visualisation of LangGraph state and event stream.
     - Management of sandboxes and deployed “first apps”.
2. **Agent Runtime (AR)** – Python 3.12 + LangGraph
   - Responsibilities:
     - Implements the “First Engineer” LangGraph.
     - Manages build threads (ideas → specs → code → tests → deploy).
     - Interfaces with external tools: SCM, CI/CD, sandbox runners, vector stores.
3. **Sandbox Manager (SM)** – infra/service abstraction
   - Responsibilities:
     - Receives build artifacts and spins up isolated execution environments for generated apps.
     - Provides logs, metrics, and teardown APIs.
     - Enforces security and resource limits (namespaces, containers, VMs).

**Communication pattern.**

- OC ↔ AR: **HTTPS JSON APIs + Server-Sent Events (SSE)** for streaming.
- OC ↔ SM: HTTPS JSON APIs, plus WebSocket or SSE for live logs/metrics.
- AR ↔ SM: HTTPS (internal) API / gRPC for high-volume operations, plus queue (e.g., SQS / PubSub) for long-running build and test workloads.

---

### 3.3 Monorepo Directory Layout

Target layout (top-level):

```text
/ (repo root)
  turbo.json              # Turborepo config
  package.json            # Workspace definition for TS projects
  pyproject.toml          # Python workspace management (uv/poetry)
  .github/workflows/      # CI pipelines
  infra/                  # IaC (Terraform/Pulumi), K8s manifests, Helm charts
  docs/
    research/
      COMPLETE_ARCHITECTURE_SPEC.md
    runbooks/
    api/
  apps/
    web/                  # Owner Console (Next.js 16, Tailwind, shadcn)
    agent-api/            # Thin TS/Node API gateway -> Python AR
    agent-runtime/        # Python FastAPI service exposing LangGraph
    sandbox-manager/      # Service/API for sandbox lifecycle
  packages/
    ui/                   # shadcn-based component library
    config/               # Shared TypeScript config & env schema
    contracts/            # OpenAPI / TS client types for AR & SM
    monitoring/           # Shared logging/metrics helpers
  python_packages/
    yfe_langgraph/        # LangGraph graphs, state schemas, tools
    yfe_domain/           # Domain logic (idea parsing, spec gen, etc.)
    yfe_adapters/         # External integrations (SCM, CI, clouds)
````

**Key patterns.**

* **Separation of concerns:** LangGraph logic lives in `python_packages/yfe_langgraph`; HTTP/context boundaries are handled in `apps/agent-runtime` (FastAPI) and `apps/agent-api`.
* **Contracts first:** All external HTTP APIs (Owner Console → Agent Runtime, Owner Console → Sandbox Manager) use OpenAPI/JSON Schema definitions stored in `packages/contracts`, which generate both TS client types and Python pydantic models.
* **Infra as code:** `infra/` owns K8s manifests, DB schemas (via migrations), network policies, and secrets configuration (via an external vault).

---

### 3.4 Service API Boundaries

#### 3.4.1 Owner Console ↔ Agent Runtime

**Core endpoints (HTTP JSON + SSE).**

* `POST /v1/projects`

  * Input: idea description, owner metadata.
  * Output: project ID, initial thread ID.
* `POST /v1/projects/{project_id}/threads`

  * Input: optional initial instructions; returns a new thread ID in AR.
* `POST /v1/threads/{thread_id}/events/start-build`

  * Triggers initial LangGraph run for that thread.
* `GET /v1/threads/{thread_id}/stream` (SSE)

  * Streams `astream_events(version="v2")` from the LangGraph run.
* `POST /v1/threads/{thread_id}/actions/{action_id}`

  * Used to resume graphs after HITL interrupts with `approve`, `edit`, or `reject` decisions.

#### 3.4.2 Agent Runtime ↔ Sandbox Manager

* `POST /v1/builds`

  * Input: build artifacts (source code repo reference, build plan).
  * Output: build ID.
* `POST /v1/builds/{build_id}/deploy`

  * Deploys artifact to a sandbox environment.
* `GET /v1/builds/{build_id}/status`

  * Build + deployment status.
* `GET /v1/sandboxes/{sandbox_id}/logs` (WebSocket or SSE).

**Transport considerations.**

* Internal traffic (AR ↔ SM) runs over **mTLS-authenticated** HTTP/gRPC within a private network (Kubernetes service mesh or equivalent).
* External traffic (OC ↔ AR/SM) terminates at a gateway with WAF, rate limiting, and JWT-based auth.

---

## 4. “First Engineer” Engine – LangGraph Design

### 4.1 State Schema (Conceptual TypedDict)

The build process is modelled as a LangGraph `StateGraph` operating on a `BuildState` structure. In implementation this will be a Python `TypedDict` or `pydantic` model; here we define the fields and types so the schema is unambiguous.

**BuildState fields.**

| Field name        | Type (Python-style)                                                                                | Description                                                                                |                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `thread_id`       | `str`                                                                                              | Logical conversation/build thread identifier (maps to checkpointer thread).                |                                                              |
| `project_id`      | `str`                                                                                              | Stable project identifier from Owner Console.                                              |                                                              |
| `idea`            | `str`                                                                                              | Original owner idea / problem statement.                                                   |                                                              |
| `requirements`    | `list[str]`                                                                                        | Normalised, model- and human-generated requirements.                                       |                                                              |
| `non_functionals` | `list[str]`                                                                                        | Explicit performance, security, compliance constraints.                                    |                                                              |
| `current_phase`   | `Literal["intake","spec","architecture","implementation","testing","deployment","done","aborted"]` | High-level workflow phase.                                                                 |                                                              |
| `messages`        | `list[BaseMessage]` or `list[dict]`                                                                | Conversation-style messages between user and agent (LangGraph `MessagesState` compatible). |                                                              |
| `system_design`   | `dict`                                                                                             | Structured system design (ERDs, service list, data flows).                                 |                                                              |
| `task_plan`       | `list[dict]`                                                                                       | Task graph for implementation (per file/module).                                           |                                                              |
| `code_artifacts`  | `list[dict]`                                                                                       | Code generation results, each with path, content hash, diff vs baseline.                   |                                                              |
| `tests`           | `list[dict]`                                                                                       | Test cases and status (unit, integration, synthetic user flows).                           |                                                              |
| `build_status`    | `Literal["pending","running","waiting_human","failed","succeeded"]`                                | Current build status.                                                                      |                                                              |
| `last_error`      | `str                                                                                               | None`                                                                                      | Last error message / failure reason, if any.                 |
| `owner_actions`   | `list[dict]`                                                                                       | Audit log of human approvals/edits/rejections.                                             |                                                              |
| `sandbox_ref`     | `dict                                                                                              | None`                                                                                      | Reference to sandbox deployment (sandbox ID, URL).           |
| `production_ref`  | `dict                                                                                              | None`                                                                                      | Reference to production deployment once “toggle” is flipped. |
| `metadata`        | `dict`                                                                                             | Miscellaneous metadata (model versions, compliance flags, etc.).                           |                                                              |

**Reducers.**

* `messages`: LangGraph `add_messages` reducer to append conversation messages.
* `owner_actions`: append reducer to maintain full HITL audit trail.
* `code_artifacts` / `tests`: append reducer, with deduplication by path/test ID inside nodes.

### 4.2 Graph Topology (Nodes & Phases)

The `StateGraph[BuildState]` uses the following conceptual nodes:

1. `intake_and_clarify`

   * Summarises the idea, asks clarifying questions, populates `requirements` and `non_functionals`.
   * May trigger HITL if requirements seem ambiguous or high-risk (EU AI Act–relevant domains, security-sensitive tasks, etc.).
2. `draft_system_design`

   * Creates `system_design` and proposes high-level architecture.
3. `review_design` (HITL)

   * Calls `interrupt()` with design summary; awaits owner approval or edits.
4. `derive_task_plan`

   * Generates `task_plan` from approved design.
5. `generate_code`

   * Iterates over tasks, generating or editing code artifacts via tools (e.g., Git provider, file APIs).
6. `run_tests`

   * Orchestrates unit tests and synthetic user flows in sandbox; records results in `tests` and updates `build_status`.
7. `qa_gate` (HITL)

   * Presents test results and diff summary; waits for owner decision to fix issues or proceed toward deployment.
8. `deploy_to_sandbox`

   * Calls Sandbox Manager to build and deploy the app; fills `sandbox_ref`.
9. `production_toggle`

   * Either auto-approves based on policy (Phase 3) or requires explicit owner approval to promote to production (`production_ref`).

The graph allows cycles between `generate_code`, `run_tests`, and `qa_gate` to refine the application iteratively.

### 4.3 Persistence – Checkpointer

**Requirement.** Durable, queryable, multi-tenant persistence of LangGraph state with support for:

* Resuming from interrupts and failures.
* Auditing decisions.
* EU AI Act–style traceability and logging.

**Decision.** **PostgreSQL-based checkpointer using `langgraph-checkpoint-postgres`.**

* Database: `PostgreSQL >= 15` (managed, e.g., RDS/Aurora/Cloud SQL).
* Library: `langgraph-checkpoint-postgres==3.0.x`, using `PostgresSaver` / `AsyncPostgresSaver` from this package.
* Policy:

  * Checkpointer configured per tenant/project namespace.
  * Full retention of checkpoints for audit and replay (with policy-based retention windows).
  * No non-JSON-serializable objects stored in metadata to avoid known serialization issues.

### 4.4 Streaming – Delivering `astream_events` to the Frontend

**Mechanism.**

* Agent Runtime uses `graph.astream_events(input, config, version="v2", stream_mode="values")` (exact mode may vary per UX needs).
* FastAPI provides an SSE endpoint (`/v1/threads/{thread_id}/stream`) that:

  * Obtains an async generator from `astream_events`.
  * Transforms each event into a compact JSON representation intended for the UI (e.g., `{ "event": "...", "data": {...}, "ts": ... }`).
  * Writes `event:` / `data:` records over SSE.
* Owner Console connects via EventSource and feeds events into a client-side state machine that renders:

  * Token-level output for chat/LLM content.
  * Progress for build stages and tests.
  * HITL prompts when `interrupt` events arrive.

**Rationale.**

* SSE is simpler than WebSockets, easier to secure and cache, and maps naturally to `astream_events` push-only event flow. If live bi-directional streaming becomes necessary, we can add WebSockets in parallel, but SSE is sufficient for the initial architecture.

### 4.5 Human-in-the-Loop (HITL) – Interrupt Pattern

**Mechanism.**

* Nodes that require human intervention call `interrupt(payload)` where `payload` includes:

  * `action_id` (stable identifier for this decision point),
  * `thread_id`, `project_id`,
  * `kind` (e.g., `"design_review"`, `"qa_gate"`, `"dangerous_tool_call"`),
  * recommended action(s) and explanation.
* When `interrupt()` is invoked:

  * LangGraph persists the current state via the Postgres checkpointer and returns an interrupt event via `astream_events`.
  * The Agent Runtime surfaces that to the Owner Console via SSE.
* The Owner Console:

  * Displays a decision UI bound to `action_id` and decision options (approve, edit, reject).
  * Records the owner’s decision as an `owner_actions` entry via `POST /v1/threads/{thread_id}/actions/{action_id}`.
* The Agent Runtime:

  * Looks up the associated thread and interrupt checkpoint.
  * Issues a command/resume call into LangGraph using the stored state and the human decision.

**Compliance note.**

* This pattern is aligned with EU AI Act Article 14 (human oversight) by design: critical steps cannot proceed without an explicit, logged human decision where required, and decisions are traceable via `owner_actions`.

---

## 5. Security & Compliance Mapping (High Level)

This section maps the architecture to major security and compliance frameworks. Detailed control-by-control mapping will be done by the Security Architecture team.

### 5.1 OWASP ASVS 5.0

* Use ASVS 5.0 as the baseline application security requirement set for Owner Console, Agent Runtime APIs, and Sandbox Manager.
* Target **Level 2** for all Internet-facing services; Level 3 for any high-risk or regulated tenants.
* Key implications:

  * Strong authN/authZ, including MFA and least-privilege service accounts.
  * Input/output validation at all API boundaries (typed contracts in `packages/contracts`, pydantic validation on backend).
  * Secure session management and CSRF protection on Owner Console.
  * Explicit hardening of secret management, TLS configuration, and DB access.

### 5.2 OWASP LLM Top 10 (2025)

* **Prompt injection & insecure output handling:** Tools invoked by the agent (e.g., filesystem, SCM, CI) are constrained by strict policies and validated inputs; tool calls requiring higher privileges are guarded by HITL interrupts.
* **Training data & prompt leakage:** Logs and checkpointer data are treated as confidential; no direct echoing of sensitive content back to other tenants.
* **Supply chain & model management:** Model choices and versions are tracked in `metadata` within `BuildState`; infrastructure for model access uses least-privilege API keys and secrets.

### 5.3 NIST CSF 2.0 & NIST SSDF (SP 800-218)

* CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover) are supported by:

  * Clear asset inventory (services, models, sandboxes) via infra-as-code and observability.
  * Central logging of all LangGraph events, HITL decisions, and deployment actions.
  * Runbooks in `docs/runbooks/` for incident response and recovery.
* SSDF alignment:

  * `Prepare` – Threat modelling for each feature set; security requirements included in user stories.
  * `Protect` – Secure coding practices + automated SAST/DAST as part of the monorepo CI.
  * `Produce` – Mandatory code review, dependency scanning, and signing of container images.
  * `Respond` – Centralised vulnerability handling and playbooks for patch/rollback.

### 5.4 ISO/IEC 42001 & EU AI Act

* ISO/IEC 42001: Use as the AI management system framework for risk management, governance, and documentation around YFE’s AI components.
* EU AI Act:

  * Assume many YFE workloads fall under “limited risk” but design for possible **high-risk** classification (e.g., if apps are used in finance, hiring, or safety-critical settings).
  * Architecture supports:

    * Logging and traceability (checkpointer + sandbox logs).
    * Human oversight at key decision points (interrupt-based HITL).
    * Technical documentation for models and workflows (via `docs/` and structured metadata).

---

## 6. Delivery Roadmap

### Phase 1 – MVP (“Production Toggle Proof”)

**Objective:** Prove that YFE can take a non-trivial idea → generate an app → deploy to sandbox → promote to a stable “production” environment with human approval.

**Scope:**

* Monorepo skeleton with:

  * `apps/web` (simple Owner Console with project creation, live stream viewer, and approval UI).
  * `apps/agent-runtime` (LangGraph-based engine with `BuildState`, intake → design → code → sandbox deploy).
  * `apps/sandbox-manager` (minimal, e.g., single cluster with namespace-per-sandbox).
* Basic LangGraph workflow:

  * `intake_and_clarify` → `draft_system_design` → `derive_task_plan` → `generate_code` → `deploy_to_sandbox` → `production_toggle`.
  * Simple tests (smoke test only) and one HITL gate at the final production toggle.
* Streaming via SSE from `astream_events(version="v2")` to Owner Console.

**Exit criteria:**

* Owner can enter a simple idea (e.g., “Issue tracker with login and CRUD for tickets”) and, within a bounded time, see a working demo app in a sandbox and explicitly approve promotion to a small production cluster.

### Phase 2 – Scale (“Synthetic User QA”)

**Objective:** Upgrade YFE from linear build to robust iterative refinement using automated synthetic QA.

**Scope:**

* Extended LangGraph with `run_tests` and `qa_gate` phases.
* Synthetic user scenarios represented as structured tests in `tests` within `BuildState`.
* Sandboxes extended to support load tests, regression test suites, and performance checks.
* Owner Console gets:

  * Visual test results and diff visualisation.
  * Policy configs: e.g., “auto-fix minor issues” vs “require approval for all changes”.

**Exit criteria:**

* For a class of apps (e.g., CRUD + workflows), YFE can run synthetic QA, auto-iterate to fix simple issues, and present only the final diff + results for owner approval.

### Phase 3 – Market Leader (“Full Autonomy under Policy”)

**Objective:** Enable policy-driven autonomy where human oversight is focused on high-risk decisions, not every build step.

**Scope:**

* Policy engine defining where HITL is mandatory vs optional (per tenant, per project domain, per risk level).
* Multi-tenant support with per-tenant isolation at data, sandbox, and checkpointer levels.
* Advanced observability: tracing (Langfuse or similar), structured metrics, anomaly detection on build behaviour.
* Integration with enterprise IAM, ticketing (Jira, Linear), and SCM/CI systems.

**Exit criteria:**

* For low-risk domains and tenants that accept it, YFE can autonomously build, test, and deploy updates within predefined guardrails, while maintaining auditability for EU AI Act and internal governance requirements.

---

## 7. Naming Conventions

**General principles.**

* `kebab-case` for folders and file names (TS/JS).
* `snake_case` for Python modules and functions.
* `PascalCase` for React components, Python classes, and LangGraph node wrappers.
* `SCREAMING_SNAKE_CASE` for constants and environment variables.

### 7.1 Services

* Owner Console app: `apps/web`
* Agent Runtime API gateway: `apps/agent-api`
* Agent Runtime service: `apps/agent-runtime`
* Sandbox Manager: `apps/sandbox-manager`
* Python domain packages:

  * `yfe_langgraph`
  * `yfe_domain`
  * `yfe_adapters`

### 7.2 LangGraph

* Graphs: `BuildGraph`, `ReviewGraph`, etc. (suffix `Graph`).
* Nodes: verbs in `snake_case` for implementation functions (e.g., `draft_system_design`) and `PascalCase` for node objects if wrapped in classes.
* State schemas: `BuildState`, `ChatState` etc.
* Checkpointers: `postgres_checkpointer` variable, `PostgresCheckpointConfig` type.

### 7.3 APIs & Contracts

* REST resources: plural nouns, e.g., `/v1/projects`, `/v1/threads`, `/v1/builds`, `/v1/sandboxes`.
* Events: `event_type` enums like `BUILD_PHASE_CHANGED`, `INTERRUPT_REQUESTED`, `TEST_RESULTS_UPDATED`.
* TypeScript types in `packages/contracts` named `Project`, `Thread`, `Build`, `Sandbox`, `StreamEvent`.

---

## 8. Implementation Roadmap (High-Level Steps)

1. **Bootstrap monorepo & infra**

   * Owners: Platform Eng + Infra.
   * Deliver: Turborepo structure, base Next.js 16 app, Python workspace, dev/prod clusters, Postgres, and basic CI.
2. **Implement baseline Agent Runtime**

   * Owners: Agent Eng.
   * Deliver: `BuildState` schema, minimal `StateGraph`, FastAPI endpoints, Postgres checkpointer integration, SSE streaming of `astream_events`.
3. **Implement Owner Console v1**

   * Owners: Frontend Eng.
   * Deliver: Project creation UI, build monitor view, basic HITL decision UI, SSE integration.
4. **Implement Sandbox Manager v1**

   * Owners: Infra + Runtime.
   * Deliver: API for build/deploy/list logs; single-cluster sandbox isolation.
5. **Security & compliance hardening**

   * Owners: Security Eng.
   * Deliver: ASVS 5.0 L2 checklist, OWASP LLM Top 10 mitigations, logging/traceability for EU AI Act alignment.
6. **Synthetic QA & iterative loop (Phase 2)**

   * Owners: Agent Eng + QA.
   * Deliver: `run_tests`, `qa_gate` nodes, synthetic user scenario modelling, UI for QA results.
7. **Policy-driven autonomy (Phase 3)**

   * Owners: Product + Agent Eng.
   * Deliver: Policy engine, HITL configuration, extended observability and multi-tenant isolation.

---

## 9. Open Questions & Assumptions

* Exact cloud provider and managed services (DB, K8s, queues) are left to the Infra team but must support managed Postgres, container orchestration, and secure secret management.
* Model providers (OpenAI, Anthropic, local models) are abstracted behind `langchain-core` interfaces; final selection is a separate brief.
* Sandbox security hardening (e.g., syscall filters, network egress policies) and language/runtime support for generated apps will evolve with early customer needs.

This specification is intended as a **baseline law**: downstream Architecture, Security, and Data teams should elaborate on their parts but not contradict the core stack decisions and service boundaries without an explicit change record.

````

```csv
filename="evidence/G1/comparative-matrix.csv"
OptionID,Category,OptionName,Description,Pros,Cons,RiskLevel,TCO_3yr,Performance,Primary
frontend_next15,Frontend,Next.js 15,Previous major Next.js version with stable App Router and React 19 support.,"Mature, well-understood; fewer surprises; large community base.","Shorter remaining lifecycle; misses Next 16 caching & performance features; future upgrade required.",LOW,MEDIUM,MEDIUM,FALSE
frontend_next16,Frontend,Next.js 16,"Current major release with stable React Compiler, Turbopack default, improved caching and routing.","Best long-term support; faster builds & reloads; better caching control; strong App Router story.","Requires Node 20.9+; Turbopack still maturing for edge cases; some early-adopter issues possible.",MEDIUM,LOW,HIGH,TRUE
css_tailwind3,CSS,Tailwind CSS 3.x,Stable utility-first CSS framework using JS-based config.,"Very mature ecosystem; many examples; simple mental model for existing teams.","Will eventually be superseded; migration to v4 can be non-trivial; fewer new features over time.",LOW,MEDIUM,MEDIUM,FALSE
css_tailwind4,CSS,Tailwind CSS 4.x,Next-generation Tailwind with CSS-first config and new CLI.,"Future-proof; streamlined config; already used in modern Next.js templates.","Breaking changes vs v3; some docs and tools still catching up; more complex initial setup.",MEDIUM,LOW,HIGH,TRUE
ui_shadcn_single,UI,shadcn/ui single-app,Use shadcn components generated directly into the Owner Console app.,"Simple initial setup; minimal monorepo coordination.","Harder to reuse across apps; duplication as more apps are added; inconsistent UX risk.",MEDIUM,MEDIUM,MEDIUM,FALSE
ui_shadcn_shared,UI,shadcn/ui shared package,"Generate shadcn components into a shared @yfe/ui package for reuse.","Consistent design system; single place for upgrades; aligns with monorepo best practices.","Requires slightly more setup; need governance over changes.",LOW,LOW,HIGH,TRUE
repo_poly,Repo,Polyrepo,"Separate repos per service (web, agent-runtime, sandbox).","Clear isolation and permissions; simpler per-repo CI.","Slow cross-cutting changes; contract drift; duplicated tooling.",MEDIUM,MEDIUM,MEDIUM,FALSE
repo_turbo,Repo,Monorepo with Turborepo,"Single repo with Turborepo orchestrating TS + Python tasks.","Excellent DX for Next.js; simple shared packages; atomic changes.","Requires careful cache config; Turborepo expertise needed.",LOW,LOW,HIGH,TRUE
repo_nx,Repo,Monorepo with Nx,"Polyglot monorepo using Nx generators and task graph.","Rich tooling; good for complex polyglot estates.","More friction with Next.js-standard tooling; smaller overlap with Vercel ecosystem defaults.",MEDIUM,MEDIUM,MEDIUM,FALSE
py311,Runtime,Python 3.11,Previous baseline version widely used in production.,"Maximum compatibility; most libraries test here first.","Shorter remaining support horizon; eventually requires upgrade.",LOW,MEDIUM,MEDIUM,FALSE
py312,Runtime,Python 3.12,Mainstream modern Python with performance improvements over 3.11.,"Good balance of stability and future-proofing; wide ecosystem support.","Slightly smaller install base than 3.11; some older libs may lag.",LOW,LOW,HIGH,TRUE
py313,Runtime,Python 3.13,Latest major version with further optimisations.,"Most future-proof; best long-term support window.","Ecosystem adoption still ramping; some libs may not fully support yet.",MEDIUM,LOW,HIGH,FALSE
cp_inmem,Persistence,InMemorySaver,In-memory LangGraph checkpointer.,"Great for development and tests; zero infra.","Not durable; no multi-instance support; unsuitable for production.",HIGH,LOW,HIGH,FALSE
cp_postgres,Persistence,Postgres checkpointer,"PostgreSQL-backed checkpointer via langgraph-checkpoint-postgres.","Durable; scalable; recommended for production; supports HIL and replay.","Requires DB ops; schema migrations; need to manage retention.",LOW,MEDIUM,HIGH,TRUE
stream_ws,Streaming,WebSocket,"Full-duplex streaming channel between browser and backend.","Supports client->server streaming; flexible.","More complex infra; harder to debug and cache; not always needed.",MEDIUM,MEDIUM,HIGH,FALSE
stream_sse,Streaming,Server-Sent Events (SSE),"HTTP-based uni-directional streaming from backend to browser.","Simple; fits astream_events pattern; easy to secure and deploy.","No client->server streaming; limited browser support quirks in older UAs.",LOW,LOW,HIGH,TRUE
hitl_ad_hoc,HITL,Ad-hoc approvals,Manual flags in application code to trigger UI prompts.,"Easy to bolt on initially.","Hard to reason about; poor traceability; fragile.",HIGH,MEDIUM,MEDIUM,FALSE
hitl_interrupt,HITL,LangGraph interrupt-based HITL,"Use LangGraph interrupt() + checkpointer for human-in-the-loop decisions.","First-class HIL support; great traceability; easy resumption.","Requires careful UX and state management; more upfront design.",LOW,LOW,HIGH,TRUE
````

```json
filename="evidence/G1/decisions.json"
{
  "schemaVersion": "1.1",
  "briefId": "YFE-ARCH-001",
  "createdAt": "2025-11-21T00:00:00Z",
  "decisions": [
    {
      "id": "stack.frontend",
      "title": "Frontend framework and runtime",
      "status": "accepted",
      "option": "frontend_next16",
      "rationale": "Use Next.js 16 with Node 20.9+ to align with current major line, App Router stability, and future-proof performance features including React Compiler and Turbopack.",
      "alternatives": [
        "frontend_next15"
      ],
      "impacts": [
        "Owner Console",
        "Monorepo toolchain"
      ],
      "riskLevel": "MEDIUM"
    },
    {
      "id": "stack.css",
      "title": "CSS framework",
      "status": "accepted",
      "option": "css_tailwind4",
      "rationale": "Tailwind 4 is chosen for a greenfield project to avoid near-term migration from 3.x and align with modern Next.js/shadcn templates.",
      "alternatives": [
        "css_tailwind3"
      ],
      "impacts": [
        "Owner Console",
        "Shared UI library"
      ],
      "riskLevel": "MEDIUM"
    },
    {
      "id": "stack.ui",
      "title": "UI library model",
      "status": "accepted",
      "option": "ui_shadcn_shared",
      "rationale": "A shared @yfe/ui package maximises reuse and design consistency across multiple apps in the monorepo.",
      "alternatives": [
        "ui_shadcn_single"
      ],
      "impacts": [
        "Owner Console",
        "Future apps"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "stack.repo",
      "title": "Repository structure",
      "status": "accepted",
      "option": "repo_turbo",
      "rationale": "A Turborepo monorepo offers the best DX for Next.js 16 and shadcn, while still supporting Python services via custom tasks.",
      "alternatives": [
        "repo_poly",
        "repo_nx"
      ],
      "impacts": [
        "All services",
        "CI/CD"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "stack.runtime",
      "title": "Python runtime version",
      "status": "accepted",
      "option": "py312",
      "rationale": "Python 3.12 balances ecosystem maturity and long-term support while being fully compatible with LangGraph 1.0.3.",
      "alternatives": [
        "py311",
        "py313"
      ],
      "impacts": [
        "Agent Runtime",
        "Python tooling"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "stack.persistence",
      "title": "LangGraph persistence backend",
      "status": "accepted",
      "option": "cp_postgres",
      "rationale": "PostgreSQL-based checkpointer is recommended by LangGraph for production and aligns with traceability and auditability requirements.",
      "alternatives": [
        "cp_inmem"
      ],
      "impacts": [
        "Agent Runtime",
        "Compliance"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "stack.streaming",
      "title": "Streaming transport to frontend",
      "status": "accepted",
      "option": "stream_sse",
      "rationale": "SSE is simpler to operate and maps directly to astream_events' push-only event model, covering current UX needs.",
      "alternatives": [
        "stream_ws"
      ],
      "impacts": [
        "Owner Console",
        "Agent Runtime"
      ],
      "riskLevel": "LOW"
    },
    {
      "id": "stack.hitl",
      "title": "Human-in-the-loop mechanism",
      "status": "accepted",
      "option": "hitl_interrupt",
      "rationale": "LangGraph interrupt-based HIL provides durable, auditable pauses and resumption, aligning with EU AI Act human oversight obligations.",
      "alternatives": [
        "hitl_ad_hoc"
      ],
      "impacts": [
        "Agent Runtime",
        "Compliance"
      ],
      "riskLevel": "LOW"
    }
  ]
}
```

```text
filename="evidence/G1/checksums.txt"
docs/research/COMPLETE_ARCHITECTURE_SPEC.md  sha256=d1d250b1b7702413014e8b3e0dc2028087625c793480da604bf8f14dc08a16c3
evidence/G1/comparative-matrix.csv          sha256=371d6de6711d690ed14197d5ab14d990011aedef10354b85d1fcd79cd1193576
evidence/G1/decisions.json                  sha256=9a0425450f720bdebd58cb9887073d5a6a4230393ae267f557ef9b8662718c77
```

---

### Notes on Key Evidence (out-of-band, for validation)

* **Next.js 16**: official release notes and upgrade guide describe stable React Compiler support, Turbopack default, and Node.js ≥ 20.9.0 & TypeScript ≥ 5.1.0 as hard requirements. ([nextjs.org][1])
* **Tailwind 4**: v4 introduces a CSS-first configuration model and new CLI, with breaking changes vs v3 and official migration guidance. ([tailwindcss.com][2])
* **shadcn/ui**: documented as a code generator (not a traditional library) with official CLI, monorepo support, and deep integration with Next.js and Tailwind. ([ui.shadcn.com][3])
* **LangGraph 1.0.3**: current stable LangGraph v1.x on PyPI with dependencies and guidance to use Postgres-based checkpointers for production. ([pypistats.org][4])
* **Python & compliance frameworks**: Python 3.13 stability and LangGraph compatibility, NIST CSF 2.0, NIST SSDF SP 800-218, OWASP ASVS 5.0 RC / 5.0, OWASP LLM Top 10 2025, ISO/IEC 42001 and EU AI Act documentation are used as the basis for security and governance mapping. ([Python.org][5])

---

```text
=== RESULT FROM RA ===
BriefID: YFE-ARCH-001 | Seq: 1 | Gate: G1 | StateHash: NA
Status: PASS
Evidence:
  - docs/research/COMPLETE_ARCHITECTURE_SPEC.md (sha256=d1d250b1b7702413014e8b3e0dc2028087625c793480da604bf8f14dc08a16c3)
  - evidence/G1/decisions.json (sha256=9a0425450f720bdebd58cb9887073d5a6a4230393ae267f557ef9b8662718c77)
  - evidence/G1/comparative-matrix.csv (sha256=371d6de6711d690ed14197d5ab14d990011aedef10354b85d1fcd79cd1193576)
  - evidence/G1/checksums.txt (sha256=cb7d250534bc39598ae63374787a4a2d7a7db3f8255865c05303bf15bb970a1b)
Notes: Primary recommendation is a Turborepo monorepo with Next.js 16 / Tailwind 4 / shadcn and a Python 3.12 LangGraph 1.0.3 Agent Runtime using Postgres-based checkpointing, SSE streaming, and interrupt-based HITL. Main risks are early-adopter aspects of Next.js 16/Tailwind 4 and policy/infra work for EU AI Act alignment; mitigations are canary environments, strict version pinning, and security-by-design practices mapped to ASVS, NIST CSF, SSDF, ISO 42001, and EU AI Act.
=== END RESULT ===
```

[1]: https://nextjs.org/blog/next-16?utm_source=chatgpt.com "Next.js 16"
[2]: https://tailwindcss.com/blog/tailwindcss-v4?utm_source=chatgpt.com "Tailwind CSS v4.0"
[3]: https://ui.shadcn.com/docs/monorepo?utm_source=chatgpt.com "Monorepo - shadcn/ui"
[4]: https://pypistats.org/packages/langgraph?utm_source=chatgpt.com "langgraph"
[5]: https://www.python.org/downloads/release/python-3130/?utm_source=chatgpt.com "Python Release Python 3.13.0"
