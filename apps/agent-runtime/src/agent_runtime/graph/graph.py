from typing import Any
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

from ..settings import settings
from ..schemas.state import AgentState
# Import nodes inside create_graph or here if circular deps not an issue.
# The nodes import get_llm from here, so we might have a circular dependency if we import nodes here at top level
# and nodes import get_llm from here.
# To avoid circular dependency, get_llm should be in a separate file or nodes should import it inside the function?
# Or better, put get_llm in a separate utils file?
# The instructions say: "Extract get_llm -> graph/graph.py" and "Update create_graph in graph/graph.py with new imports".
# And nodes import `from ..graph import get_llm`.
# If graph/graph.py imports nodes, and nodes import graph/graph.py, that's a cycle.
# Solution: Move get_llm to a separate file or use lazy imports.
# However, the instruction says "Extract get_llm -> graph/graph.py".
# Let's check if I can put get_llm in graph/graph.py and import nodes inside create_graph?
# Or import nodes at the top but they import get_llm from here.
# Python handles circular imports if they are not used at module level.
# Nodes use get_llm inside the function. So it might be fine if get_llm is defined before imports? No.
# Let's try to follow the instruction but be careful.
# Actually, the instruction says:
# # graph/nodes/planning.py
# from ..graph import get_llm
#
# # graph/graph.py
# from .nodes.planning import planner_node
#
# This is a circular import.
# I will place get_llm in `graph/llm.py` to avoid this, or I will accept the cycle if it works (it often doesn't).
# Wait, the instruction explicitly says:
# "Extract get_llm -> graph/graph.py"
# "Update create_graph in graph/graph.py with new imports"
#
# If I put get_llm in graph/graph.py, and nodes import it, and graph.py imports nodes...
# I will put imports of nodes INSIDE create_graph to avoid top-level cycle.

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

def create_graph(checkpointer: Any) -> Any:
    """Create and return compiled LangGraph."""
    # Import nodes here to avoid circular dependency with get_llm
    from .nodes.planning import planner_node
    from .nodes.execution import executor_node

    # Build graph using ONLY patterns from MCP queries
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)

    return workflow.compile(checkpointer=checkpointer)
