from typing import TypedDict, Literal
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """State for the agent graph."""
    schema_version: Literal["1"]  # NEW: Version tracking
    task: str
    plan: str | None
    result: str | None
    messages: list[BaseMessage]
