"""Tests for Synthetic QA Nodes."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent_runtime.graph.nodes.test_evaluator import test_evaluator_node as evaluator_node_impl
from agent_runtime.graph.nodes.test_executor import take_screenshot
from agent_runtime.graph.nodes.test_executor import test_executor_node as executor_node_impl
from agent_runtime.graph.nodes.test_planner import test_planner_node as planner_node_impl
from agent_runtime.schemas.state import AgentState

# --- Test Planner Tests ---

@pytest.mark.asyncio
async def test_planner_node_success():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value.content = """
    ```json
    {
        "steps": [
            {"action": "navigate", "url": "http://localhost:3000"},
            {"action": "click", "selector": "#submit"}
        ]
    }
    ```
    """

    with patch("agent_runtime.graph.nodes.test_planner.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_planner.get_stream_writer",
             return_value=MagicMock()
         ):

        state = AgentState(task="Test Task", result="Done", messages=[])
        result = await planner_node_impl(state)

        assert "test_plan" in result
        assert len(result["test_plan"]["steps"]) == 2
        assert result["test_plan"]["steps"][0]["action"] == "navigate"

@pytest.mark.asyncio
async def test_planner_node_failure():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.side_effect = Exception("LLM Error")

    with patch("agent_runtime.graph.nodes.test_planner.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_planner.get_stream_writer",
             return_value=MagicMock()
         ):

        state = AgentState(task="Test Task", result="Done", messages=[])
        result = await planner_node_impl(state)

        assert "test_plan" in result
        assert result["test_plan"]["steps"] == []

# --- Test Executor Tests ---

@pytest.fixture
def mock_toolkit():
    toolkit = MagicMock()
    tools = {
        "navigate_browser": MagicMock(name="navigate_browser"),
        "click_element": MagicMock(name="click_element"),
        "extract_text": MagicMock(name="extract_text"),
        "get_elements": MagicMock(name="get_elements"),
    }
    # Setup default returns
    tools["navigate_browser"].run.return_value = "Navigated"
    tools["click_element"].run.return_value = "Clicked"
    tools["get_elements"].run.return_value = "Found elements"

    # get_tools returns list of tools
    tool_objs = []
    for name, mock_tool in tools.items():
        mock_tool.name = name
        tool_objs.append(mock_tool)

    toolkit.get_tools.return_value = tool_objs
    return toolkit

@pytest.mark.asyncio
async def test_executor_node_all_actions(mock_toolkit):
    # Setup screenshot tool mock
    with patch("agent_runtime.graph.nodes.test_executor.get_toolkit", return_value=mock_toolkit), \
         patch(
             "agent_runtime.graph.nodes.test_executor.get_stream_writer",
             return_value=MagicMock()
         ), \
         patch("agent_runtime.graph.nodes.test_executor.take_screenshot") as mock_screenshot:

        mock_screenshot.invoke.return_value = "Screenshot saved to screenshots/test.png"

        state = AgentState(
            task="Test Task",
            test_plan={
                "steps": [
                    {"action": "navigate", "url": "http://localhost:3000"},
                    {"action": "click", "selector": "#btn"},
                    # Should pass but do nothing/log
                    {"action": "fill", "selector": "#input", "value": "text"},
                    {"action": "screenshot", "name": "step1"},
                    {"action": "assert_text", "selector": ".msg", "text": "Success"},
                    {"action": "unknown_action", "data": "foo"}
                ]
            },
            messages=[]
        )

        # Mock get_elements to return text containing "Success"
        tools = {t.name: t for t in mock_toolkit.get_tools()}
        tools["get_elements"].run.return_value = "<div>Success</div>"

        result = await executor_node_impl(state)

        steps = result["test_results"]["steps"]
        assert len(steps) == 6

        # Navigate
        assert steps[0]["action"] == "navigate"
        assert steps[0]["passed"] is True

        # Click
        assert steps[1]["action"] == "click"
        assert steps[1]["passed"] is True

        # Fill (implementation is pass)
        assert steps[2]["action"] == "fill"
        # It falls through to elif action == "fill": pass -> then what?
        # Wait, the code has `elif action == "fill": pass`.
        # It does NOT set step_result["passed"] = True inside the block.
        # It initializes `passed=False`. So it should be False?
        # Let's check the code.
        # step_result = { ..., "passed": False, ... }
        # elif action == "fill": pass
        # So it remains False.
        assert steps[2]["passed"] is False

        # Screenshot
        assert steps[3]["action"] == "screenshot"
        assert steps[3]["passed"] is True
        assert "test.png" in result["screenshots"][0]

        # Assert Text
        assert steps[4]["action"] == "assert_text"
        assert steps[4]["passed"] is True

        # Unknown
        assert steps[5]["action"] == "unknown_action"
        assert steps[5]["passed"] is False
        assert "Unknown action" in steps[5]["output"]

@pytest.mark.asyncio
async def test_executor_node_exception(mock_toolkit):
    with patch("agent_runtime.graph.nodes.test_executor.get_toolkit", return_value=mock_toolkit), \
         patch(
             "agent_runtime.graph.nodes.test_executor.get_stream_writer",
             return_value=MagicMock()
         ):

        # Make navigate fail
        tools = {t.name: t for t in mock_toolkit.get_tools()}
        tools["navigate_browser"].run.side_effect = Exception("Browser Crash")

        state = AgentState(
            task="Test Task",
            test_plan={"steps": [{"action": "navigate", "url": "http://fail.com"}]},
            messages=[]
        )

        result = await executor_node_impl(state)

        steps = result["test_results"]["steps"]
        assert steps[0]["passed"] is False
        assert "Browser Crash" in steps[0]["output"]

def test_take_screenshot_tool():
    # Mock toolkit and browser context
    mock_toolkit = MagicMock()
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()

    mock_toolkit.sync_browser = mock_browser
    mock_browser.contexts = [mock_context]
    mock_context.pages = [mock_page]

    with patch("agent_runtime.graph.nodes.test_executor.get_toolkit", return_value=mock_toolkit), \
         patch("os.makedirs"):

        # Test success
        result = take_screenshot.invoke({"name": "test_shot"})
        assert "Screenshot saved to" in result
        mock_page.screenshot.assert_called_once()

        # Test no pages
        mock_context.pages = []
        result = take_screenshot.invoke({"name": "test_shot_no_page"})
        assert "No active page" in result

        # Test exception
        mock_toolkit.sync_browser = None # Cause AttributeError
        result = take_screenshot.invoke({"name": "test_crash"})
        assert "Failed to take screenshot" in result

# --- Test Evaluator Tests ---

@pytest.mark.asyncio
async def test_evaluator_node_success():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value.content = '{"tests_passed": true, "test_report": "Good"}'

    with patch("agent_runtime.graph.nodes.test_evaluator.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_evaluator.get_stream_writer",
             return_value=MagicMock()
         ):

        state = AgentState(
            task="Test Task",
            test_results={"steps": [{"passed": True}]},
            messages=[]
        )

        result = await evaluator_node_impl(state)
        assert result["tests_passed"] is True

@pytest.mark.asyncio
async def test_evaluator_node_no_steps():
    with patch(
        "agent_runtime.graph.nodes.test_evaluator.get_stream_writer",
        return_value=MagicMock()
    ):
        state = AgentState(
            task="Test Task",
            test_results={"steps": []},
            messages=[]
        )
        result = await evaluator_node_impl(state)
        assert result["tests_passed"] is False
        assert "No test steps" in result["test_report"]

@pytest.mark.asyncio
async def test_evaluator_node_parsing_formats():
    mock_llm = AsyncMock()

    # Test markdown json
    mock_llm.ainvoke.return_value.content = '```json\n{"tests_passed": true}\n```'
    with patch("agent_runtime.graph.nodes.test_evaluator.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_evaluator.get_stream_writer",
             return_value=MagicMock()
         ):
        result = await evaluator_node_impl(AgentState(test_results={"steps": [{}]}))
        assert result["tests_passed"] is True

    # Test plain backticks
    mock_llm.ainvoke.return_value.content = '```\n{"tests_passed": true}\n```'
    with patch("agent_runtime.graph.nodes.test_evaluator.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_evaluator.get_stream_writer",
             return_value=MagicMock()
         ):
        result = await evaluator_node_impl(AgentState(test_results={"steps": [{}]}))
        assert result["tests_passed"] is True

@pytest.mark.asyncio
async def test_evaluator_node_failure():
    mock_llm = AsyncMock()
    mock_llm.ainvoke.side_effect = Exception("LLM Fail")

    with patch("agent_runtime.graph.nodes.test_evaluator.get_llm", return_value=mock_llm), \
         patch(
             "agent_runtime.graph.nodes.test_evaluator.get_stream_writer",
             return_value=MagicMock()
         ):

        result = await evaluator_node_impl(AgentState(test_results={"steps": [{}]}))
        assert result["tests_passed"] is False
        assert "Evaluation failed" in result["test_report"]
