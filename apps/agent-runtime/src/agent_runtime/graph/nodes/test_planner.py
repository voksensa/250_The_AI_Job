"""Test Planner Node."""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ...utils.logger import get_logger
from ...utils.telemetry import get_meter
from ..graph import get_llm

logger = get_logger(__name__)
meter = get_meter(__name__)
node_executions = meter.create_counter("graph_node_executions", description="Graph node executions")

TEST_PLANNER_PROMPT = """
You are a QA Engineer. Your goal is to create a simple, happy-path test plan
to verify that a task was completed successfully.

Task: {task}
Execution Result: {result}

Generate a JSON test plan with a list of steps.
Supported actions:
- "navigate": {{"url": "http://localhost:3000/..."}}
- "click": {{"selector": "button#submit"}}
- "fill": {{"selector": "input#name", "value": "test"}}
- "assert_text": {{"selector": "div.result", "text": "Success"}}
- "screenshot": {{"name": "step_name"}}

Keep it simple. Focus on verifying the main outcome.
Return ONLY the JSON object with a "steps" key.
Example:
{{
  "steps": [
    {{"action": "navigate", "url": "http://localhost:3000"}},
    {{"action": "fill", "selector": "input#todo", "value": "Buy milk"}},
    {{"action": "click", "selector": "button#add"}},
    {{"action": "screenshot", "name": "after_add"}}
  ]
}}
"""

async def test_planner_node(state: AgentState) -> dict[str, Any]:
    """Generate a test plan based on the task and result."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="test_planner", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "test_planner", "status": "started"})

    writer = get_stream_writer()
    writer({"status": "planning_tests", "message": "Generating test plan..."})

    llm = get_llm()

    task = state.get("task", "")
    result = state.get("result", "")

    messages = [
        SystemMessage(content="You are a QA test planner."),
        HumanMessage(content=TEST_PLANNER_PROMPT.format(task=task, result=result))
    ]

    try:
        response = await llm.ainvoke(messages)
        content = response.content

        # Basic JSON parsing (robustness improvements can be added later)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        test_plan = json.loads(content)

        logger.info(
            "node_execution",
            node="test_planner",
            status="complete",
            plan_steps=len(test_plan.get("steps", [])),
            task_id=task_id
        )
        node_executions.add(1, {"node_name": "test_planner", "status": "completed"})

        writer({"status": "test_planned", "test_plan": test_plan})
        return {"test_plan": test_plan}

    except Exception as e:
        logger.error(
            "node_execution_failed",
            node="test_planner",
            error=str(e),
            task_id=task_id,
            exc_info=True
        )
        node_executions.add(1, {"node_name": "test_planner", "status": "failed"})
        # Fallback to empty plan or re-raise? For now, let's return empty to avoid crashing graph,
        # but the next node should handle empty plan.
        return {"test_plan": {"steps": []}}
