from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ...utils.logger import get_logger
from ...utils.telemetry import get_meter
from ..graph import get_llm

logger = get_logger(__name__)
meter = get_meter(__name__)
node_executions = meter.create_counter("graph_node_executions", description="Graph node executions")


async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    task_id = state.get("task", "unknown")
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

        prompt_message = HumanMessage(
            content=f"Execute this plan:\n\n{plan}\n\nProvide implementation details."
        )
        messages = state['messages'] + [prompt_message]

        response = await llm.ainvoke(messages)
        result = response.content
        logger.info(
            "node_execution",
            node="executor",
            status="complete",
            result_length=len(result),
            task_id=task_id
        )
        node_executions.add(1, {"node_name": "executor", "status": "completed"})

        writer({"status": "completed", "result": result})
        return {"result": str(result), "messages": [response]}
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
