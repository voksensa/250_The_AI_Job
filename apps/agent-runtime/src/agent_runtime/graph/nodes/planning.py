from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ...utils.logger import get_logger
from ..graph import get_llm

logger = get_logger(__name__)


async def planner_node(state: AgentState) -> dict[str, Any]:
    """Create a plan from task description."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="planner", status="starting", task_id=task_id)
    
    writer = get_stream_writer()
    writer({"status": "planning", "message": "Generating plan..."})

    # Use real LLM
    llm = get_llm()

    messages = [
        HumanMessage(content=f"Create a brief execution plan for this task: {state['task']}")
    ]

    response = await llm.ainvoke(messages)
    plan = response.content
    logger.info("node_execution", node="planner", status="complete", plan_length=len(plan), task_id=task_id)

    writer({"status": "planned", "plan": plan})
    return {"plan": str(plan), "messages": [response]}
