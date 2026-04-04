"""
Provider tool for ai-system.

Calls the configured provider routing layer to execute a prompt.
"""

import logging
from typing import Any, Dict

from controller.agent_controller import AgentController
from tools.base import Tool

logger = logging.getLogger(__name__)


class ProviderTool(Tool):
    """Tool that routes prompts through the configured provider chain."""

    def __init__(self, controller: AgentController):
        self.controller = controller

    @property
    def name(self) -> str:
        return "call_provider"

    @property
    def description(self) -> str:
        return "Route a prompt through the configured provider chain and return the result."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Prompt text to send to the provider chain."
                }
            },
            "required": ["prompt"]
        }

    def execute(self, prompt: str) -> str:
        logger.info("Executing provider tool")
        task = {"prompt": prompt}
        result = self.controller.run_task(task)

        if result.get("success"):
            return result.get("result", "")

        error_code = result.get("error_code", "UNKNOWN_ERROR")
        error_message = result.get("result", "No result returned")
        raise RuntimeError(f"Provider execution failed: {error_code}: {error_message}")
