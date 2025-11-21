from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    task: str
    plan: Optional[Dict[str, Any]]
    code: Optional[Dict[str, str]]
    status: str
    messages: List[Any]
