
import json
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, WebSocket
from fastapi.encoders import jsonable_encoder

from ...schemas.api.tasks import TaskRequest, TaskResponse

router = APIRouter()

@router.post("/v1/tasks", response_model=TaskResponse)
async def create_task(
    request: Request,
    task_request: TaskRequest,
    background_tasks: BackgroundTasks
):
    """Create and start a new task."""
    task_id = str(uuid.uuid4())
    graph = request.app.state.graph

    config = {"configurable": {"thread_id": task_id}}
    # NEW: Add schema_version
    inputs = {
        "schema_version": "1",
        "task": task_request.task,
        "messages": []
    }

    background_tasks.add_task(run_graph_background, graph, inputs, config)

    return {"task_id": task_id, "status": "running"}

async def run_graph_background(graph: Any, inputs: dict[str, Any], config: dict[str, Any]):
    """Helper to run graph in background."""
    try:
        async for _ in graph.astream(inputs, config=config, stream_mode="values"):
            pass
    except Exception as e:
        print(f"Error in background task: {e}")

@router.get("/v1/tasks/{task_id}")
async def get_task_status(request: Request, task_id: str):
    """Get current task state from checkpointer."""
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": task_id}}
    try:
        state = await graph.aget_state(config)
        if not state.values:
            raise HTTPException(status_code=404, detail="Task not found")
        return state.values
    except HTTPException:
        raise
    except Exception as e:
        # This will be caught by the global exception handler and converted to RFC 9457
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.websocket("/v1/tasks/{task_id}/stream")
async def stream_task(websocket: WebSocket, task_id: str):
    """Stream real-time task execution events."""
    await websocket.accept()
    graph = websocket.app.state.graph

    config = {"configurable": {"thread_id": task_id}}

    # If the task hasn't started yet, we might need to pass inputs.
    # For this MVP, we assume the client calls POST /tasks first,
    # OR we allow starting via websocket if inputs are provided.
    # We'll assume the task is already running or we are just attaching to the stream.
    # However, astream works best when driving the execution.

    # Let's support running via WebSocket for the "Stream" experience.
    # The client sends the task description, we run and stream back.

    try:
        data = await websocket.receive_text()
        message = json.loads(data)
        task_input = message.get("task")

        # NEW: Add schema_version if starting new task
        # NEW: Add schema_version if starting new task
        inputs = None
        if task_input:
             inputs = {
                "schema_version": "1",
                "task": task_input,
                "messages": []
            }
        elif message.get("production_approved"):
            # Resume graph execution
            print(f"DEBUG: Resuming graph for task {task_id} with approval")
            inputs = None # Resume with no new inputs, just continue
            # We might need to update state if we weren't using interrupt_before logic that assumes the node does the work.
            # But here, we just want to resume.
            # However, astream(None, config) might not work if it expects inputs?
            # For resuming from interrupt, we usually pass Command or None.
            # Let's try passing None.
            pass

        if inputs is not None or message.get("production_approved"):
            async for chunk in graph.astream(
                inputs,
                config=config,
                stream_mode=["updates", "custom"]
            ):
                # chunk is a tuple (mode, payload) when stream_mode is a list
                if isinstance(chunk, tuple):
                    mode, payload = chunk
                    # Flatten for frontend convenience or send structured
                    # Frontend expects {lint_status: ...} directly in the payload for custom events
                    if mode == "custom":
                        await websocket.send_json(jsonable_encoder(payload))
                    elif mode == "updates":
                        # updates payload is {node_name: state_update}
                        # We might want to send this too
                        await websocket.send_json(jsonable_encoder(payload))
                else:
                    await websocket.send_json(jsonable_encoder(chunk))

    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
