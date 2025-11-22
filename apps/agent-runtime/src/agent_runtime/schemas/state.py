from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State for the agent graph."""
    schema_version: Literal["1"]  # NEW: Version tracking
    task: str
    plan: str | None
    result: str | None
    lint_status: str | None  # "pass" | "fail"
    test_status: str | None  # "pass" | "fail"
    production_approved: bool | None  # True if approved
    deployment_url: str | None  # URL of deployed app
    messages: list[BaseMessage]
