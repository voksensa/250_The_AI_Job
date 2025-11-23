import os
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ...utils.logger import get_logger
from ...utils.telemetry import get_meter
from ..graph import get_llm

logger = get_logger(__name__)
meter = get_meter(__name__)
node_executions = meter.create_counter("graph_node_executions", description="Graph node executions")

@tool
def create_file(filename: str, content: str, task_id: str) -> str:
    """Create a file in task workspace.
    
    Args:
        filename: Name of the file to create (e.g., 'hello.py')
        content: Content to write to the file
        task_id: ID of the task (used for directory isolation)
    """
    workspace = f"/workspace/{task_id}"
    os.makedirs(workspace, exist_ok=True)
    filepath = os.path.join(workspace, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return f"Created {filename} ({len(content)} bytes)"

async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    task_id = state.get("task_id", "unknown")
    logger.info("node_execution", node="executor", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "executor", "status": "started"})

    writer = get_stream_writer()
    writer({"status": "executing", "message": "Executing plan..."})

    # Check if plan exists
    plan = state.get("plan")
    if not plan:
        logger.error("execution_error", node="executor", error="No plan generated", task_id=task_id)
        node_executions.add(1, {"node_name": "executor", "status": "failed"})
        return {"result": "Error: No plan was generated"}

    try:
        # Use real LLM for execution
        llm = get_llm()

        # Bind tools
        llm_with_tools = llm.bind_tools([create_file])

        prompt_message = HumanMessage(
            content=f"""Task: {state.get("task")}
Plan: {plan}

Generate actual working files for this task.
Use the create_file tool to write each file.
Pass task_id='{task_id}' to the tool.
Return structured file list, NOT explanations."""
        )
        messages = state['messages'] + [prompt_message]

        response = await llm_with_tools.ainvoke(messages)

        # Execute tool calls
        files_created = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "create_file":
                    args = tool_call["args"]
                    # Ensure task_id is present
                    if "task_id" not in args:
                        args["task_id"] = task_id

                    # Execute tool
                    create_file.invoke(args)
                    files_created.append(args["filename"])
                    logger.info("file_created", filename=args["filename"], task_id=task_id)

        result_summary = f"Created {len(files_created)} files: {', '.join(files_created)}"
        if not files_created:
            # Fallback to text if no files created (shouldn't happen with strict prompt)
            result_summary = response.content

        logger.info(
            "node_execution",
            node="executor",
            status="complete",
            result_length=len(result_summary),
            task_id=task_id
        )
        node_executions.add(1, {"node_name": "executor", "status": "completed"})

        writer({"status": "completed", "result": result_summary})
        return {"result": result_summary, "messages": [response]}
    except Exception as e:
        logger.error(
            "execution_error",
            node="executor",
            error=str(e),
            task_id=task_id,
            exc_info=True
        )
        node_executions.add(1, {"node_name": "executor", "status": "failed"})
        raise
