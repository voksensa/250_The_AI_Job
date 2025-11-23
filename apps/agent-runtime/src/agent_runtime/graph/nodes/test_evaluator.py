"""Test Evaluator Node."""

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

EVALUATOR_PROMPT = """
You are a QA Lead. Evaluate the results of a synthetic user test run.

Test Plan & Results:
{results}

Determine if the test passed or failed based on the step outputs.
- If all critical steps (navigation, actions, assertions) succeeded, mark as PASSED.
- If any critical step failed or showed an error, mark as FAILED.
- Provide a brief, human-readable report summarizing what happened.

Return ONLY a JSON object:
{{
  "tests_passed": true/false,
  "test_report": "Summary of the test run..."
}}
"""

async def test_evaluator_node(state: AgentState) -> dict[str, Any]:
    """Evaluate test results."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="test_evaluator", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "test_evaluator", "status": "started"})

    writer = get_stream_writer()
    writer({"status": "evaluating_tests", "message": "Analyzing test results..."})

    test_results = state.get("test_results", {})

    # Quick check: if no steps, fail?
    if not test_results.get("steps"):
        logger.warning("test_evaluator_no_steps", task_id=task_id)
        return {
            "tests_passed": False,
            "test_report": "No test steps were executed."
        }

    llm = get_llm()

    # Format results for LLM
    results_str = json.dumps(test_results, indent=2)

    messages = [
        SystemMessage(content="You are a QA evaluator."),
        HumanMessage(content=EVALUATOR_PROMPT.format(results=results_str))
    ]

    try:
        response = await llm.ainvoke(messages)
        content = response.content

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        evaluation = json.loads(content)
        tests_passed = evaluation.get("tests_passed", False)
        test_report = evaluation.get("test_report", "No report generated.")

        logger.info(
            "node_execution",
            node="test_evaluator",
            status="complete",
            passed=tests_passed,
            task_id=task_id
        )
        node_executions.add(1, {"node_name": "test_evaluator", "status": "completed"})

        writer({
            "status": "test_evaluation_complete",
            "passed": tests_passed,
            "report": test_report
        })

        return {
            "tests_passed": tests_passed,
            "test_report": test_report
        }

    except Exception as e:
        logger.error(
            "node_execution_failed",
            node="test_evaluator",
            error=str(e),
            task_id=task_id,
            exc_info=True
        )
        node_executions.add(1, {"node_name": "test_evaluator", "status": "failed"})
        return {
            "tests_passed": False,
            "test_report": f"Evaluation failed: {str(e)}"
        }
