import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from .types import AgentState
import os

# Connection string for Postgres
DB_URI = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

# Node implementations


async def planner_node(state: AgentState) -> Dict[str, Any]:
    """Planning node that creates a simple plan."""
    print(f"--- PLANNER NODE: Processing task '{state['task']}' ---")
    # Simulate LLM planning
    await asyncio.sleep(1)
    return {
        "plan": {"steps": ["analyze", "code", "verify"]},
        "status": "planning_complete",
        "messages": ["Plan created"]
    }


async def coder_node(state: AgentState) -> Dict[str, Any]:
    """Coding node that generates code."""
    print("--- CODER NODE: Generating code ---")
    # Simulate LLM coding
    await asyncio.sleep(1)
    return {
        "code": {"main.py": "print('Hello World')"},
        "status": "coding_complete",
        "messages": ["Code generated"]
    }


async def responder_node(state: AgentState) -> Dict[str, Any]:
    """Responder node that finalizes the task."""
    print("--- RESPONDER NODE: Finalizing ---")
    return {
        "status": "completed",
        "messages": ["Task completed successfully"]
    }

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("responder", responder_node)

# Add edges
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "responder")
workflow.add_edge("responder", END)

# Set entry point
workflow.set_entry_point("planner")

# Setup checkpointer
pool = ConnectionPool(conninfo=DB_URI)
checkpointer = PostgresSaver(pool)
checkpointer.setup()

# Compile the graph
graph = workflow.compile(checkpointer=checkpointer)
