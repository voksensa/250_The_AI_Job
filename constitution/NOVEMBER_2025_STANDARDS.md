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
