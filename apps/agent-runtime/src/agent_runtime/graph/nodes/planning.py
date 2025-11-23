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


async def planner_node(state: AgentState) -> dict[str, Any]:
    """Create a plan from task description."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="planner", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "planner", "status": "started"})

    writer = get_stream_writer()
    writer({"status": "planning", "message": "Generating plan..."})

    # Use real LLM
    llm = get_llm()

    messages = [
        HumanMessage(content=f"Create a brief execution plan for this task: {state['task']}")
    ]

    response = await llm.ainvoke(messages)
    plan = response.content
    logger.info(
        "node_execution",
        node="planner",
        status="complete",
        plan_length=len(plan),
        task_id=task_id
    )
    node_executions.add(1, {"node_name": "planner", "status": "completed"})

    writer({"status": "planned", "plan": plan})
    return {"plan": str(plan), "messages": [response]}
