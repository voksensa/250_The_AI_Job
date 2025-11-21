# Implementation Plan - Restore Agent Runtime Service

**Goal**: Restore the `apps/agent-runtime` service to a working state by implementing the missing `api/routes.py` and `graph.py` files, strictly adhering to native LangGraph 1.0.3 patterns verified by MCP research.

## User Review Required
> [!IMPORTANT]
> This plan implements the core logic for the Agent Runtime. It uses `PostgresSaver` for state persistence and `astream` with `stream_mode=["updates", "custom"]` for real-time events, as verified in the research phase.

## Proposed Changes

### apps/agent-runtime

#### [NEW] [api/__init__.py](file:///Users/Yousef_1/Downloads/250_The_AI_Job/apps/agent-runtime/src/agent_runtime/api/__init__.py)
- Empty file to make `api` a package.

#### [NEW] [api/routes.py](file:///Users/Yousef_1/Downloads/250_The_AI_Job/apps/agent-runtime/src/agent_runtime/api/routes.py)
- **Endpoints**:
  - `POST /tasks`: Starts a new task in the background.
  - `GET /tasks/{task_id}`: Retrieves task state from `PostgresSaver`.
  - `WebSocket /tasks/{task_id}/stream`: Streams events using `graph.astream`.
- **Dependencies**: Imports `create_graph` from `..graph`.

#### [NEW] [graph.py](file:///Users/Yousef_1/Downloads/250_The_AI_Job/apps/agent-runtime/src/agent_runtime/graph.py)
- **State**: `AgentState` (TypedDict).
- **Nodes**:
  - `planner_node`: Generates a plan using LLM.
  - `executor_node`: Executes the plan (simulated/real LLM call).
- **Graph**: `StateGraph` compiled with `PostgresSaver`.
- **Streaming**: Uses `get_stream_writer` for custom events.

## Verification Plan

### Automated Tests
1.  **Service Startup**:
    ```bash
    cd apps/agent-runtime
    uvicorn agent_runtime.main:app --reload
    # Expect: Startup successful, no import errors
    ```
2.  **Static Analysis**:
    ```bash
    ruff check src/
    mypy src/ --ignore-missing-imports
    # Expect: No errors
    ```

### Manual Verification
1.  **End-to-End Task**:
    - Send `POST /api/tasks` with a task description.
    - Verify response contains `task_id`.
    - Check `GET /api/tasks/{task_id}` for status updates.
    - Verify data persists in Postgres `checkpoints` table.
2.  **Streaming**:
    - Connect to WebSocket endpoint and verify JSON chunks are received.
