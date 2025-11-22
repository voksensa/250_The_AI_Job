# Constitutional Files Audit Matrix

| File | Domain | Key Content | Overlaps | Status | Last Updated |
|------|--------|-------------|----------|--------|--------------|
| `ARCHITECTURAL_DECISIONS.md` | Architecture | 5 non-negotiable rules (API v1, Error format, State schema, Folder layout, Naming), 6 validated patterns. | Overlaps with `NOVEMBER_2025_STANDARDS.md` (linting), `STATE_MANAGEMENT.md` (state schema). | **Active** (Enforced Phase 1) | Unknown (Implied recent) |
| `ENGINE_ARCHITECTURE_V1.md` | Architecture | Defines "First Engineer" agent graph, nodes (Planner, CodeGenerator, TestRunner), and flow. Replaces `langgraph_mapping.md`. | Replaces `langgraph_mapping_depreciated.md`. | **Active** | Unknown (Implied recent) |
| `EXECUTION_PROTOCOL_SPEC.md` | Process | Execution protocol, task templates, evidence collection, quality gates G1-G11 checklists. | Overlaps with `NOVEMBER_2025_STANDARDS.md` (gates), `CLAUDE.md` (gates). | **Active** | Unknown (Implied recent) |
| `NOVEMBER_2025_STANDARDS.md` | Standards | Tool versions (Node 22, ESLint 9.39, Python 3.11+), Gate thresholds (Coverage 80%/70%). | Overlaps with `GOLDEN_RULES.md` (coverage), `ARCHITECTURAL_DECISIONS.md` (linting). | **Active** | 2025-11-21 |
| `OPERATIONAL_CONTEXT.md` | Documentation | Navigation guide, directory structure, key files, tech stack summary. | Overlaps with `VISION.md`, `STRATEGY.md`, `ROADMAP_SPEC.md`. | **Active** | 2025-11-20 |
| `ROADMAP_SPEC.md` | Product | Roadmap P0-P5, success criteria, deliverables, timeline. | Overlaps with `STRATEGY.md` (phases), `VISION.md` (goals). | **Active** | Unknown (Implied recent) |
| `STATE_MANAGEMENT.md` | Process | "Goldfish Memory" solution, state files (INDEX, CURRENT_TASK), handoff protocols. | Overlaps with `EXECUTION_PROTOCOL_SPEC.md` (process). | **Active** | 2025-11-21 |
| `STRATEGY.md` | Product | Business strategy, 3 killer features (Toggle, QA, Story), pricing, competitive edge. | Overlaps with `VISION.md`, `ROADMAP_SPEC.md`. | **Active** | Nov 2025 |
| `VISION.md` | Product | North Star vision, "Your First Engineer", 3 killer features. | Overlaps with `STRATEGY.md`. | **Active** | Unknown (Implied recent) |
| `langgraph_mapping_depreciated.md` | Architecture | **DEPRECATED** visual builder plan. | Replaced by `ENGINE_ARCHITECTURE_V1.md`. | **Deprecated** | 2025-11-20 |
| `session_summary.md` | History | Summary of the "Steve Jobs" pivot session. Context for `ENGINE_ARCHITECTURE_V1.md`. | None. | **Archive** | Unknown (Implied recent) |
| `GOLDEN_RULES.md` | Standards | 4 non-negotiable rules: Diamond Rule, Coverage 85%, Production from Line 1, No Big-Bang Refactors. | Overlaps with `NOVEMBER_2025_STANDARDS.md` (coverage). | **Active** | 2025-11-22 |
