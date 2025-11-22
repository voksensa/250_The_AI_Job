from typing import Any, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

from .settings import settings


# --- State Definition ---
class AgentState(TypedDict):
    """State for the agent graph."""
    task: str
    plan: str | None
    result: str | None
    messages: list[BaseMessage]

# --- Nodes ---

def get_llm() -> ChatAnthropic | ChatOpenAI:
    """Get configured LLM based on settings."""
    if "claude" in settings.model_name.lower():
        return ChatAnthropic(
            model_name=settings.model_name,
            api_key=SecretStr(settings.anthropic_api_key),
            timeout=None,
            stop=None
        )
    return ChatOpenAI(
        model=settings.model_name,
        api_key=SecretStr(settings.openai_api_key)
    )

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

async def executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the plan."""
    writer = get_stream_writer()
    writer({"status": "executing", "message": "Executing plan..."})
    print(f"DEBUG: Starting executor_node with plan: {state['plan'][:100]}...")

    # Use real LLM for execution
    # Use real LLM for execution
    llm = get_llm()

    messages = state['messages'] + [
        HumanMessage(content=f"Execute this plan: {state['plan']}. Return the result.")
    ]

    response = await llm.ainvoke(messages)
    print(f"DEBUG: Executor response: {response.content[:100]}...")
    result = response.content

    writer({"status": "completed", "result": result})
    return {"result": str(result), "messages": [response]}

# --- Graph Construction ---

def create_graph(checkpointer: Any) -> Any:
    """Create and return compiled LangGraph."""
    # Build graph using ONLY patterns from MCP queries
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)

    return workflow.compile(checkpointer=checkpointer)
