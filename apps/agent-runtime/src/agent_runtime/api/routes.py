from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
from .graph import graph
from .types import AgentState

router = APIRouter()


class TaskRequest(BaseModel):
    description: str


class TaskResponse(BaseModel):
    task_id: str
    status: str


@router.post("/tasks/run", response_model=TaskResponse)
async def submit_task_run(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    initial_state: AgentState = {
        "task": request.description,
        "plan": None,
        "code": None,
        "status": "submitted",
        "messages": []
    }

    config = {"configurable": {"thread_id": task_id}}

    async def run_graph():
        await graph.ainvoke(initial_state, config=config)

    background_tasks.add_task(run_graph)

    return {"task_id": task_id, "status": "processing"}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a task."""
    config = {"configurable": {"thread_id": task_id}}

    # Get the latest state
    try:
        state_snapshot = await graph.aget_state(config)
        if not state_snapshot.values:
            return {"task_id": task_id, "status": "not_found"}

        current_state = state_snapshot.values
        status = current_state.get("status", "unknown")

        return {
            "task_id": task_id,
            "status": status,
            "state": current_state
        }
    except Exception as e:
        # If state doesn't exist or error
        return {"task_id": task_id, "status": "error", "details": str(e)}
