from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ..graph import get_llm


async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    writer = get_stream_writer()
    writer({"status": "executing", "message": "Executing plan..."})
    print(f"DEBUG: Starting executor_node with plan: {state.get('plan', '')[:100]}...")

    # Use real LLM for execution
    # Use real LLM for execution
    llm = get_llm()

    # Check if plan exists
    plan = state.get("plan")
    if not plan:
        return {"result": "Error: No plan was generated"}

    prompt_message = HumanMessage(
        content=f"Execute this plan:\n\n{plan}\n\nProvide implementation details."
    )
    messages = state['messages'] + [prompt_message]

    response = await llm.ainvoke(messages)
    print(f"DEBUG: Executor response: {response.content[:100]}...")
    result = response.content

    writer({"status": "completed", "result": result})
    return {"result": str(result), "messages": [response]}
