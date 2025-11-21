
import json
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, WebSocket
from pydantic import BaseModel

router = APIRouter()

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    task_id: str
    status: str

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    request: Request,
    task_request: TaskRequest,
    background_tasks: BackgroundTasks
):
    """Create and start a new task."""
    task_id = str(uuid.uuid4())
    graph = request.app.state.graph

    config = {"configurable": {"thread_id": task_id}}
    inputs = {"task": task_request.task, "messages": []}

    background_tasks.add_task(run_graph_background, graph, inputs, config)

    return {"task_id": task_id, "status": "running"}

async def run_graph_background(graph: Any, inputs: dict[str, Any], config: dict[str, Any]):
    """Helper to run graph in background."""
    try:
        async for _ in graph.astream(inputs, config=config, stream_mode="values"):
            pass
    except Exception as e:
        print(f"Error in background task: {e}")

@router.get("/tasks/{task_id}")
async def get_task_status(request: Request, task_id: str):
    """Get current task state from checkpointer."""
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": task_id}}
    try:
        state = await graph.aget_state(config)
        if not state:
            raise HTTPException(status_code=404, detail="Task not found")
        return state.values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.websocket("/tasks/{task_id}/stream")
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

        inputs = None if not task_input else {"task": task_input, "messages": []}

        if inputs:
            async for chunk in graph.astream(
                inputs,
                config=config,
                stream_mode=["updates", "custom"]
            ):
                # chunk is a tuple or dict depending on mode.
                # stream_mode=["updates", "custom"] yields different things.

                # We serialize and send
                # Note: LangGraph chunks might need processing to be JSON serializable
                await websocket.send_json(str(chunk))
                # Using str() for safety, ideally json.dumps with default=str

    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
