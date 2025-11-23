"""Tests for Legacy Nodes."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent_runtime.graph.nodes.execution import executor_node
from agent_runtime.graph.nodes.planning import planner_node
from agent_runtime.schemas.state import AgentState


@pytest.mark.asyncio
async def test_planner_node_legacy():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value.content = "Plan content"

    with patch("agent_runtime.graph.nodes.planning.get_llm", return_value=mock_llm), \
         patch("agent_runtime.graph.nodes.planning.get_stream_writer", return_value=MagicMock()):

        state = AgentState(task="Test Task", messages=[])
        result = await planner_node(state)

        assert result["plan"] == "Plan content"

@pytest.mark.asyncio
async def test_executor_node_legacy_success():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value.content = "Execution Result"

    with patch("agent_runtime.graph.nodes.execution.get_llm", return_value=mock_llm), \
         patch("agent_runtime.graph.nodes.execution.get_stream_writer", return_value=MagicMock()):

        state = AgentState(task="Test Task", plan="Some Plan", messages=[])
        result = await executor_node(state)

        assert result["result"] == "Execution Result"

@pytest.mark.asyncio
async def test_executor_node_legacy_no_plan():
    with patch("agent_runtime.graph.nodes.execution.get_stream_writer", return_value=MagicMock()):
        state = AgentState(task="Test Task", messages=[])
        result = await executor_node(state)
        assert "Error" in result["result"]
