import pytest
from agent_runtime.graph import planner_node, coder_node, responder_node
from agent_runtime.types import AgentState

@pytest.mark.asyncio
async def test_planner_node():
    state: AgentState = {
        "task": "test task",
        "plan": None,
        "code": None,
        "status": "submitted",
        "messages": []
    }
    result = await planner_node(state)
    assert result["status"] == "planning_complete"
    assert "plan" in result
    assert result["plan"]["steps"] == ["analyze", "code", "verify"]

@pytest.mark.asyncio
async def test_coder_node():
    state: AgentState = {
        "task": "test task",
        "plan": {"steps": ["analyze", "code", "verify"]},
        "code": None,
        "status": "planning_complete",
        "messages": []
    }
    result = await coder_node(state)
    assert result["status"] == "coding_complete"
    assert "code" in result
    assert "main.py" in result["code"]

@pytest.mark.asyncio
async def test_responder_node():
    state: AgentState = {
        "task": "test task",
        "plan": {"steps": ["analyze", "code", "verify"]},
        "code": {"main.py": "print('Hello')"},
        "status": "coding_complete",
        "messages": []
    }
    result = await responder_node(state)
    assert result["status"] == "completed"
