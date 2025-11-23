from unittest.mock import MagicMock, mock_open, patch

import pytest
from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_executor_creates_real_files():
    state = {
        "task": "hello world py",
        "task_id": "test-123",
        "plan": "Create hello.py",
        "messages": []
    }

    mock_llm = MagicMock()
    mock_response = AIMessage(
        content="Created files",
        tool_calls=[{
            "name": "create_file",
            "args": {"filename": "hello.py", "content": "print('Hello')", "task_id": "test-123"},
            "id": "call_1"
        }]
    )
    # Mock the async ainvoke method
    mock_llm.bind_tools.return_value.ainvoke = MagicMock(return_value=mock_response)
    # Make it awaitable
    async def async_return():
        return mock_response
    mock_llm.bind_tools.return_value.ainvoke.side_effect = lambda x: async_return()

    m_open = mock_open()

    # We need to patch where create_file is defined or used.
    # Since create_file is in the same module as executor_node,
    # patching builtins.open should work for the tool execution
    # IF the tool execution happens in the same process/context.

    # Import first to ensure module is loaded
    import agent_runtime.graph.nodes.execution

    with patch("agent_runtime.graph.nodes.execution.get_llm", return_value=mock_llm), \
         patch("agent_runtime.graph.nodes.execution.os.makedirs") as mock_makedirs, \
         patch(
             "agent_runtime.graph.nodes.execution.os.path.join",
             return_value="/workspace/test-123/hello.py"
         ), \
         patch(
             "agent_runtime.graph.nodes.execution.get_stream_writer",
             return_value=MagicMock()
         ), \
         patch("builtins.open", m_open):

        result = await agent_runtime.graph.nodes.execution.executor_node(state)

        # Verify tool was called and file operations happened
        mock_makedirs.assert_called_with("/workspace/test-123", exist_ok=True)
        m_open.assert_called_with("/workspace/test-123/hello.py", "w")
        m_open().write.assert_called_with("print('Hello')")
        assert "Created 1 files" in result["result"]

@pytest.mark.asyncio
async def test_executor_no_plan():
    state = {"task": "foo", "task_id": "123", "messages": []}
    # Import first to ensure module is loaded
    import agent_runtime.graph.nodes.execution

    with patch("agent_runtime.graph.nodes.execution.get_stream_writer", return_value=MagicMock()):
        result = await agent_runtime.graph.nodes.execution.executor_node(state)
        assert "Error: No plan" in result["result"]

@pytest.mark.asyncio
async def test_executor_missing_task_id_in_tool():
    state = {
        "task": "hello",
        "task_id": "test-123",
        "plan": "Create hello.py",
        "messages": []
    }

    mock_llm = MagicMock()
    mock_response = AIMessage(
        content="Created files",
        tool_calls=[{
            "name": "create_file",
            "args": {"filename": "hello.py", "content": "print('Hello')"}, # Missing task_id
            "id": "call_1"
        }]
    )
    mock_llm.bind_tools.return_value.ainvoke = MagicMock(return_value=mock_response)
    async def async_return(): return mock_response
    mock_llm.bind_tools.return_value.ainvoke.side_effect = lambda x: async_return()

    m_open = mock_open()

    import agent_runtime.graph.nodes.execution

    with patch("agent_runtime.graph.nodes.execution.get_llm", return_value=mock_llm), \
         patch("agent_runtime.graph.nodes.execution.os.makedirs") as mock_makedirs, \
         patch(
             "agent_runtime.graph.nodes.execution.os.path.join",
             return_value="/workspace/test-123/hello.py"
         ), \
         patch(
             "agent_runtime.graph.nodes.execution.get_stream_writer",
             return_value=MagicMock()
         ), \
         patch("builtins.open", m_open):

        await agent_runtime.graph.nodes.execution.executor_node(state)

        # Verify task_id was injected
        mock_makedirs.assert_called_with("/workspace/test-123", exist_ok=True)

@pytest.mark.asyncio
async def test_executor_no_files_created():
    state = {
        "task": "hello",
        "task_id": "test-123",
        "plan": "Just explain",
        "messages": []
    }

    mock_llm = MagicMock()
    mock_response = AIMessage(
        content="I am just explaining",
        tool_calls=[]
    )
    mock_llm.bind_tools.return_value.ainvoke = MagicMock(return_value=mock_response)
    async def async_return(): return mock_response
    mock_llm.bind_tools.return_value.ainvoke.side_effect = lambda x: async_return()

    import agent_runtime.graph.nodes.execution

    with patch("agent_runtime.graph.nodes.execution.get_llm", return_value=mock_llm), \
         patch("agent_runtime.graph.nodes.execution.get_stream_writer", return_value=MagicMock()):

        result = await agent_runtime.graph.nodes.execution.executor_node(state)
        assert result["result"] == "I am just explaining"
