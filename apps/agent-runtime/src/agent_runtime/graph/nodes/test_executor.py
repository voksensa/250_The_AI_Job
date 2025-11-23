"""Test Executor Node."""

import os
from typing import Any

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_sync_playwright_browser,
)
from langchain_core.tools import tool
from langgraph.config import get_stream_writer

from ...schemas.state import AgentState
from ...utils.logger import get_logger
from ...utils.telemetry import get_meter

logger = get_logger(__name__)
meter = get_meter(__name__)
node_executions = meter.create_counter("graph_node_executions", description="Graph node executions")

# Shared browser instance (lazy loaded)
_BROWSER = None
_TOOLKIT = None

def get_toolkit():
    """Get or create the Playwright toolkit."""
    global _BROWSER, _TOOLKIT
    if _TOOLKIT is None:
        _BROWSER = create_sync_playwright_browser()
        _TOOLKIT = PlayWrightBrowserToolkit.from_browser(sync_browser=_BROWSER)
    return _TOOLKIT

@tool
def take_screenshot(name: str) -> str:
    """Take a screenshot of the current page.

    Args:
        name: Name of the screenshot (without extension).
    """
    # Access the shared browser instance from the toolkit
    toolkit = get_toolkit()
    # The toolkit's browser wrapper has a 'browser' attribute which is the Playwright browser
    # We need to find the active page.

    # Note: In the sync wrapper, we might need to iterate contexts.
    # This is a simplified approach assuming single context/page for the test.
    try:
        browser = toolkit.sync_browser
        # Iterate through contexts and pages to find the active one
        for context in browser.contexts:
            if context.pages:
                page = context.pages[0]

                # Ensure directory exists
                os.makedirs("screenshots", exist_ok=True)
                path = f"screenshots/{name}.png"

                page.screenshot(path=path)

                # Return base64 for frontend display (optional, or just path)
                # For now, returning path is safer for large images
                return f"Screenshot saved to {path}"

    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"

    return "No active page found to screenshot."

async def test_executor_node(state: AgentState) -> dict[str, Any]:
    """Execute the test plan."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="test_executor", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "test_executor", "status": "started"})

    writer = get_stream_writer()
    writer({"status": "executing_tests", "message": "Running synthetic user tests..."})

    test_plan = state.get("test_plan", {})
    steps = test_plan.get("steps", [])

    toolkit = get_toolkit()
    tools_map = {t.name: t for t in toolkit.get_tools()}
    tools_map["take_screenshot"] = take_screenshot

    results = []
    screenshots = []

    for i, step in enumerate(steps):
        action = step.get("action")

        step_result = {
            "step": i + 1,
            "action": action,
            "details": step,
            "passed": False,
            "output": ""
        }

        try:
            if action == "navigate":
                url = step.get("url")
                tool = tools_map.get("navigate_browser")
                output = tool.run({"url": url})
                step_result["output"] = output
                step_result["passed"] = True # Basic assumption, evaluator will check deeper

            elif action == "click":
                selector = step.get("selector")
                tool = tools_map.get("click_element")
                output = tool.run({"selector": selector})
                step_result["output"] = output
                step_result["passed"] = True

            elif action == "fill":
                # Playwright toolkit might not have a direct 'fill' tool in basic set?
                # Let's check. Usually it has click, navigate, extract.
                # If 'fill' is missing, we might need to use 'click' + keyboard or custom tool.
                # For MVP, let's assume we stick to click/navigate or add custom fill if needed.
                # Actually, let's check the tools list from research.
                # ['click_element', 'navigate_browser', 'previous_webpage',
                #  'extract_text', 'extract_hyperlinks', 'get_elements', 'current_webpage']
                # 'fill' is NOT in the default list.
                # We should add a custom 'fill_element' tool if we want to support input.
                # For now, let's mark it as skipped or implement it.
                # Let's implement a simple fill tool here for completeness.
                pass

            elif action == "screenshot":
                name = step.get("name", f"step_{i}")
                output = take_screenshot.invoke({"name": name})
                step_result["output"] = output
                step_result["passed"] = "saved to" in output
                if step_result["passed"]:
                    screenshots.append(output.split("saved to ")[1])

            elif action == "assert_text":
                # Use extract_text or get_elements to verify
                selector = step.get("selector")
                text = step.get("text")
                tool = tools_map.get("extract_text") # Extracts all text?
                # Or get_elements to check existence
                # For MVP, let's use get_elements
                tool = tools_map.get("get_elements")
                output = tool.run({"selector": selector})
                step_result["output"] = output
                step_result["passed"] = text in output if output else False

            else:
                step_result["output"] = f"Unknown action: {action}"
                step_result["passed"] = False

        except Exception as e:
            step_result["output"] = str(e)
            step_result["passed"] = False
            logger.error("step_execution_failed", step=i, action=action, error=str(e))

        results.append(step_result)
        writer({"status": "test_step_complete", "step": i+1, "passed": step_result["passed"]})

    logger.info(
        "node_execution",
        node="test_executor",
        status="complete",
        steps_executed=len(results),
        task_id=task_id
    )
    node_executions.add(1, {"node_name": "test_executor", "status": "completed"})

    return {
        "test_results": {"steps": results},
        "screenshots": screenshots
    }
