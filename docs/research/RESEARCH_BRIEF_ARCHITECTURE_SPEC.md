# Research Brief: The "Your First Engineer" System Architecture

**To**: Lead Researcher / Systems Architect
**From**: The Owner
**Date**: November 21, 2025
**Priority**: Critical (Blocker for "Commit One")

## Objective
We are building "Your First Engineer" — an autonomous AI system that turns plain-language ideas into production-ready applications. We need a **definitive, evidence-based technical blueprint** to guide the engineering team.

**You are required to produce a complete architectural definition.** Nothing is assumed. Everything must be justified.

## Constraints & Mandates
1.  **LangGraph v1.0.3 (Native) ONLY**: We are NOT using v0.2 or legacy patterns. You must verify the latest "Native" patterns (e.g., `StateGraph`, `CompiledGraph`, `astream_events` v2).
2.  **FAANG-Grade Quality**: No "toy" implementations. We need production-grade error handling, persistence, and scalability.
3.  **"Goldfish Memory" Proof**: The resulting architecture must be so clear that a developer with no context can build it without asking questions.

## Required Deliverables

### 1. The Stack & Versions (Definitive Selection)
Evaluate and select the exact versions for the following. **Justify every choice** (Stability vs. Future-proofing).
*   **Frontend Framework**: Next.js 15 vs 16? (Analyze stability of App Router in 16).
*   **CSS Framework**: Tailwind 3 vs 4? (Analyze breaking changes vs. longevity).
*   **UI Library**: shadcn/ui (Which version? Monorepo compatibility?).
*   **Backend Runtime**: Python 3.11 vs 3.12+? (Compatibility with LangGraph v1.0.3).
*   **Orchestration**: LangGraph v1.0.3 (Document the exact package versions).

### 2. The Architecture (System Design)
Define the physical and logical structure of the codebase.
*   **Repository Structure**: Monorepo vs. Polyrepo? (Recommend tooling: Turborepo? Nx? Just Workspaces?).
*   **Directory Layout**: Exact folder tree (e.g., `apps/`, `packages/`, `services/`).
*   **Service Boundaries**:
    *   **Owner Console**: The UI for the user.
    *   **Agent Runtime**: The LangGraph engine.
    *   **Sandboxes**: The execution environment for generated apps.
*   **Communication**: How do they talk? (gRPC? REST? WebSocket? Shared DB?).

### 3. The "First Engineer" Engine (LangGraph Design)
Map the "Native" LangGraph v1.0.3 implementation.
*   **State Schema**: Define the `TypedDict` for the build state.
*   **Persistence**: Define the Checkpointer (PostgresSaver?).
*   **Streaming**: Define how `astream_events` reaches the frontend (Server-Sent Events? WebSockets?).
*   **Human-in-the-Loop**: Define the `interrupt` pattern for approvals.

### 4. The Roadmap (Execution Plan)
Break the build into concrete phases.
*   **Phase 1 (MVP)**: The absolute minimum to prove the "Production Toggle".
*   **Phase 2 (Scale)**: Adding "Synthetic User QA".
*   **Phase 3 (Market Leader)**: Full autonomy.

### 5. Naming Convention
*   Define the naming standard for services, folders, and classes to ensure consistency.

## Output Format
Produce a single document: `docs/research/COMPLETE_ARCHITECTURE_SPEC.md`.
This document will become the "Law" for the engineering team.
