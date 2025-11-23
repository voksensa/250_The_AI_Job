# TASK-P2-005-SYNTHETIC-QA-FOUNDATION: Synthetic User QA Engine (MVP)

**Priority**: 🔴 **HIGH** (Phase 2 Main Work)  
**Phase**: Phase 2 - Synthetic User QA  
**Estimated**: 2-3 weeks  
**Gates in Scope**: G1 (Research), G2 (Architecture), G4 (Code Quality), G5 (Tests), G10 (Owner Validation)

---

## ⚠️ CRITICAL: NATIVE FIRST MANDATE

**Before writing ANY custom code, you MUST**:
1. Search LangGraph docs for native capabilities
2. Document native options in `evidence/G1/native_research.md`
3. Justify custom code ONLY if native doesn't exist or is inferior
4. Get CEO approval if building custom solution

---

## Objective

Build MVP Synthetic User QA engine that uses LangGraph native capabilities to:
- Execute one happy-path flow (submit task → check result)
- Generate test plan from requirements
- Control browser via tool integration
- Capture screenshots and pass/fail status
- Block production toggle if tests fail

**From ROADMAP_SPEC.md** (Phase 2): "Synthetic users execute at least one happy-path flow and one error-path flow, producing click-level trace, screenshots, and structured bug reports."

---

## LangGraph Native Capabilities (VERIFIED via MCP)

### ✅ Available Native Features:

**1. Playwright Integration** ([docs.langchain.com](https://docs.langchain.com/oss/python/integrations/providers/microsoft))
- `PlayWrightBrowserToolkit` - Native LangChain integration
- Browser control (Chromium, Firefox, WebKit)
- NOT custom code - use existing toolkit

**2. Human-in-the-Loop** ([docs.langchain.com/oss/python/deepagents/human-in-the-loop))
- `interrupt()` function for approval gates
- Native LangGraph capability
- Saves state, waits for resume with `Command`

**3. Checkpointing & Persistence** ([docs.langchain.com/oss/python/langgraph/persistence))
- `AsyncPostgresSaver` (already in use)
- Automatic state persistence
- Thread-based memory across runs

**4. Custom Streaming Events** ([docs.langchain.com/oss/javascript/langgraph/streaming))
- `get_stream_writer()` (already in use)
- Stream test progress to frontend
- Native event system

**5. Tool Execution** ([docs.langchain.com/langsmith/use-tools))
- Custom tools for executing commands
- LangGraph `ToolNode` pattern
- Structured tool calling

---

## Architecture (Native LangGraph Pattern)

<truncated 5064 bytes>
