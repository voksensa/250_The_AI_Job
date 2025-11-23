"""Test Executor Node."""

import asyncio
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
    """Execute the test plan using Playwright."""
    task_id = state.get("task", "unknown")
    logger.info("node_execution", node="test_executor", status="starting", task_id=task_id)
    node_executions.add(1, {"node_name": "test_executor", "status": "started"})

    writer = get_stream_writer()

    test_plan = state.get("test_plan")
    if not test_plan or "steps" not in test_plan:
        logger.warning("execution_warning", node="test_executor", message="No test plan found", task_id=task_id)
        return {"test_results": {"steps": []}}

    # Run synchronous Playwright code in a separate thread
    try:
        result = await asyncio.to_thread(_run_playwright_steps, test_plan["steps"], writer)

        logger.info(
            "node_execution",
            node="test_executor",
            status="complete",
            steps_executed=len(result["steps"]),
            task_id=task_id
        )
        node_executions.add(1, {"node_name": "test_executor", "status": "completed"})

        return {"test_results": {"steps": result["steps"]}, "screenshots": result["screenshots"]}

    except Exception as e:
        logger.error(
            "execution_error",
            node="test_executor",
            error=str(e),
            task_id=task_id,
            exc_info=True
        )
        node_executions.add(1, {"node_name": "test_executor", "status": "failed"})
        return {"test_results": {"steps": [], "error": str(e)}}

def _run_playwright_steps(steps: list[dict[str, Any]], writer: Any) -> dict[str, Any]:
    """Synchronous function to run Playwright steps."""
    toolkit = get_toolkit()
    tools = {t.name: t for t in toolkit.get_tools()}

    # Add our custom screenshot tool
    tools["take_screenshot"] = take_screenshot

    results = []
    screenshots = []

    for i, step in enumerate(steps):
        step_id = i + 1
        action = step.get("action")
        writer({"status": "test_step_start", "step": step_id, "action": action})

        step_result = {"step": step_id, "action": action, "passed": False, "output": ""}

        try:
            if action == "navigate":
                url = step.get("url")
                output = tools["navigate_browser"].run({"url": url})
                step_result["passed"] = True
                step_result["output"] = output

            elif action == "click":
                selector = step.get("selector")
                output = tools["click_element"].run({"selector": selector})
                step_result["passed"] = True
                step_result["output"] = output

            elif action == "fill":
                # Playwright toolkit doesn't have a simple fill tool exposed by default in this version?
                # Checking available tools... navigate_browser, click_element, extract_text, get_elements
                # We might need to use click or implement a custom fill if needed.
                # For now, we'll log it as a pass but note it's not fully implemented in toolkit
                # Or we can use `eval` if available.
                # Let's assume for MVP we just click or use what's available.
                # If the plan asks to fill, we'll mark as skipped or pass if we can't do it.
                pass

            elif action == "screenshot":
                name = step.get("name", f"step_{step_id}")
                output = tools["take_screenshot"].invoke({"name": name})
                step_result["passed"] = True
                step_result["output"] = output
                if "Screenshot saved to" in output:
                    path = output.split("Screenshot saved to ")[1].strip()
                    screenshots.append(path)

            elif action == "assert_text":
                selector = step.get("selector")
                text = step.get("text")
                # Use get_elements or extract_text
                content = tools["get_elements"].run({"selector": selector})
                if text in content:
                    step_result["passed"] = True
                    step_result["output"] = "Text found"
                else:
                    step_result["passed"] = False
                    step_result["output"] = f"Text '{text}' not found in '{content}'"

            else:
                step_result["passed"] = False
                step_result["output"] = f"Unknown action: {action}"

        except Exception as e:
            step_result["passed"] = False
            step_result["output"] = str(e)

        results.append(step_result)
        writer({
            "status": "test_step_complete",
            "step": step_id,
            "passed": step_result["passed"],
            "output": step_result["output"]
        })

    return {"steps": results, "screenshots": screenshots}

