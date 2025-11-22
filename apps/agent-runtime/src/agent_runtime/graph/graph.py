from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

from ..schemas.state import AgentState
from ..settings import settings

# Import nodes inside create_graph or here if circular deps not an issue.
# The nodes import get_llm from here, so we might have a circular dependency
# if we import nodes here at top level and nodes import get_llm from here.
# To avoid circular dependency, get_llm should be in a separate file or
# nodes should import it inside the function?
# Or better, put get_llm in a separate utils file?
# The instructions say: "Extract get_llm -> graph/graph.py" and
# "Update create_graph in graph/graph.py with new imports".
# And nodes import `from ..graph import get_llm`.
# If graph/graph.py imports nodes, and nodes import graph/graph.py, that's a cycle.
# Solution: Move get_llm to a separate file or use lazy imports.
# However, the instruction says "Extract get_llm -> graph/graph.py".
# Let's check if I can put get_llm in graph/graph.py and import nodes inside create_graph?
# Or import nodes at the top but they import get_llm from here.
# Python handles circular imports if they are not used at module level.
# Nodes use get_llm inside the function. So it might be fine if get_llm is defined
# before imports? No.
# Let's try to follow the instruction but be careful.
# Actually, the instruction says:
# # graph/nodes/planning.py
# from ..graph import get_llm
#
# # graph/graph.py
# from .nodes.planning import planner_node
#
# # This is a circular import.
# # I will place get_llm in `graph/llm.py` to avoid this, or I will accept the cycle
# # if it works (it often doesn't).
# # Wait, the instruction explicitly says:
# # "Extract get_llm -> graph/graph.py"
# # "Update create_graph in graph/graph.py with new imports"
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
    from .nodes.execution import executor_node
    from .nodes.gates import (
        gate_aggregator_node,
        lint_gate_node,
        production_gate_check,
        production_interrupt_node,
        test_gate_node,
    )
    from .nodes.planning import planner_node

    # Build graph using ONLY patterns from MCP queries
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)

    # Quality Gates
    workflow.add_node("lint_gate", lint_gate_node)
    workflow.add_node("test_gate", test_gate_node)
    workflow.add_node("production_decision", production_interrupt_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")

    # Fan-out to gates
    workflow.add_edge("executor", "lint_gate")
    workflow.add_edge("executor", "test_gate")

    # Fan-in (implicit? No, we need to join. Or just check state in conditional edge)
    # LangGraph doesn't have explicit "join" node unless we make one.
    # But we can just edge from both gates to a dummy node or directly to conditional check?
    # Conditional edge must start from a node.
    # We can add a "gate_aggregator" node or just edge from both to "production_decision"
    # via conditional?
    # Wait, if we fan out, we have parallel execution.
    # We need to wait for BOTH to finish.
    # LangGraph waits for all parallel branches to finish before moving to next step
    # if they converge?
    # Let's add a "gate_check" node that does nothing but serves as synchronization point?
    # Or we can use the fact that `production_gate_check` is a conditional edge.
    # We can't put conditional edge on TWO nodes.
    # So we need a join node.

    # Fan-in to aggregator
    workflow.add_node("gate_aggregator", gate_aggregator_node)
    workflow.add_edge("lint_gate", "gate_aggregator")
    workflow.add_edge("test_gate", "gate_aggregator")

    # Conditional edge from aggregator
    workflow.add_conditional_edges(
        "gate_aggregator",
        production_gate_check,
        {
            "ready_for_production": "production_decision",
            "not_ready": "executor" # Loop back to fix
        }
    )

    workflow.add_edge("production_decision", END)

    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["production_decision"]
    )
