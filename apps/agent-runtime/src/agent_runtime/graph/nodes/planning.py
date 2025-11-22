from typing import Any
from langchain_core.messages import HumanMessage
from langgraph.config import get_stream_writer
from ...schemas.state import AgentState
from ..graph import get_llm

async def planner_node(state: AgentState) -> dict[str, Any]:
    """Create a plan from task description."""
    writer = get_stream_writer()
    writer({"status": "planning", "message": "Generating plan..."})
    print(f"DEBUG: Starting planner_node for task: {state['task']}")

    # Use real LLM
    # Use real LLM
    llm = get_llm()

    messages = [
        HumanMessage(content=f"Create a brief execution plan for this task: {state['task']}")
    ]

    response = await llm.ainvoke(messages)
    print(f"DEBUG: Planner response: {response.content[:100]}...")
    plan = response.content

    writer({"status": "planned", "plan": plan})
    return {"plan": str(plan), "messages": [response]}
