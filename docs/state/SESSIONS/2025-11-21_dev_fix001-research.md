# Session Log: Restore Agent Runtime (TASK-FIX-001) - Research

**Date**: 2025-11-21
**Topic**: Native LangGraph Patterns Research

## Research Findings

### MCP Query 1: StateGraph Basics
- **Query**: "langgraph 1.0.3 StateGraph basic example"
- **Key Finding**: 
  - Use `StateGraph(State)` where `State` is a `TypedDict`.
  - Add nodes with `.add_node(name, func)`.
  - Add edges with `.add_edge(start, end)`.
  - Compile with `.compile(checkpointer=...)`.
- **Applied To**: `graph.py` core structure.
- **Link**: https://docs.langchain.com/oss/javascript/langgraph/overview (and Python equivalents)

### MCP Query 2: PostgreSQL Checkpointer
- **Query**: "langgraph PostgresSaver checkpoint postgres setup"
- **Key Finding**:
  - Import: `from langgraph.checkpoint.postgres import PostgresSaver`
  - Setup: `checkpointer = PostgresSaver.from_conn_string("postgresql://...")`
  - Init: `checkpointer.setup()`
  - Usage: Pass to `graph.compile(checkpointer=checkpointer)`.
- **Applied To**: `graph.py` checkpointer initialization.
- **Link**: https://docs.langchain.com/oss/python/langgraph/persistence

### MCP Query 3: Streaming Events
- **Query**: "langgraph astream streaming custom events stream_mode"
- **Key Finding**:
  - Use `graph.astream(inputs, stream_mode=["updates", "custom"])`.
  - "updates" gives state changes.
  - "custom" gives events emitted by `get_stream_writer`.
- **Applied To**: `api/routes.py` WebSocket endpoint.
- **Link**: https://docs.langchain.com/oss/python/langgraph/streaming

### MCP Query 4: Custom Events with get_stream_writer
- **Query**: "langgraph get_stream_writer custom events tutorial"
- **Key Finding**:
  - Import: `from langgraph.config import get_stream_writer` (Python 3.11+).
  - Usage inside node:
    ```python
    writer = get_stream_writer()
    writer({"custom_key": "data"})
    ```
  - Requires `stream_mode="custom"` in `astream`.
- **Applied To**: `graph.py` nodes for emitting progress/results.
- **Link**: https://docs.langchain.com/oss/python/langgraph/streaming

### MCP Query 5: Human-in-the-loop
- **Query**: "langgraph interrupt human approval Command"
- **Key Finding**:
  - Use `interrupt_on` or `Command` for interrupts.
  - (Not strictly required for Phase 0 MVP but good to know for future).
- **Applied To**: Future phases.

### MCP Query 6: FastAPI Integration
- **Query**: "langgraph fastapi integration async streaming"
- **Key Finding**:
  - General guidance on streaming.
  - Use `astream` in a WebSocket endpoint.
  - Background tasks for non-blocking execution if not streaming.
- **Applied To**: `api/routes.py` structure.

## Implementation Decisions

### Decision 1: PostgresSaver Connection Pattern
- **Question**: How to initialize PostgresSaver?
- **Decision**: Use `PostgresSaver.from_conn_string` with the database URL from settings.
- **Rationale**: Native pattern verified in docs.
- **Code**: `graph.py` `create_graph` function.

### Decision 2: Streaming Pattern
- **Question**: How to stream to WebSocket?
- **Decision**: Use `async for chunk in graph.astream(..., stream_mode=["updates", "custom"])` and send JSON chunks to WebSocket.
- **Rationale**: Native `astream` support for custom events.
- **Code**: `api/routes.py` WebSocket handler.
