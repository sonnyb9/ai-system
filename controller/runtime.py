"""
Agent runtime for ai-system.

Provides a bridge between task execution, context management, and tool support.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from config import BASE_DIR, MODEL, OLLAMA_URL, TEMPERATURE, TIMEOUT, MAX_TURNS, CONTEXT_WINDOW, TOKEN_BUDGET
from controller.agent_controller import AgentController
from controller.context import ContextManager
from llm import OllamaLLM
from tools.base import ToolRegistry
from tools.file_read import FileReadTool
from tools.file_write import FileWriteTool
from tools.provider_tool import ProviderTool
from tools.system_info import SystemInfoTool

logger = logging.getLogger(__name__)


class AgentRuntime:
    """Runtime layer that orchestrates tasks, context, and tools."""

    def __init__(
        self,
        config_root: Optional[str] = None,
        max_turns: Optional[int] = None,
        context_window: Optional[int] = None,
        token_budget: Optional[int] = None,
        safe_dir: Optional[str] = None,
    ):
        self.config_root = Path(config_root or BASE_DIR)
        self.context = ContextManager(
            max_messages=context_window or CONTEXT_WINDOW,
            token_budget=token_budget or TOKEN_BUDGET,
            system_prompt=self._get_system_prompt(),
        )
        self.tools = ToolRegistry(safe_dir=safe_dir, approval_callback=self._approval_callback)
        self.controller = AgentController(str(self.config_root))
        self.tools.register(ProviderTool(self.controller))
        self.tools.register(FileReadTool(safe_dir=safe_dir))
        self.tools.register(FileWriteTool(safe_dir=safe_dir))
        self.tools.register(SystemInfoTool())
        self.llm = OllamaLLM(
            model=MODEL,
            base_url=OLLAMA_URL,
            temperature=TEMPERATURE,
            timeout=TIMEOUT,
        )
        self.max_turns = max_turns or MAX_TURNS
        logger.info("AgentRuntime initialized")

    def _get_system_prompt(self) -> str:
        return (
            "You are a task-oriented AI system assistant. "
            "Track conversation history, provider results, and available tools."
        )

    def _approval_callback(self, tool_name: str, params: Dict[str, Any]) -> bool:
        logger.info(f"Approval requested for tool '{tool_name}' with params: {params}")
        return True

    def run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        prompt = task.get("prompt", "")
        if not prompt:
            return {
                "success": False,
                "result": "",
                "error_code": "MISSING_PROMPT",
                "retriable": False,
            }

        self.context.add_message("user", prompt)

        try:
            result_text = self._process_loop()
            self.context.add_message("assistant", result_text)
            return {
                "success": True,
                "result": result_text,
                "error_code": "",
                "retriable": False,
            }
        except Exception as exc:
            logger.error(f"AgentRuntime failed: {exc}")
            error_message = str(exc)
            self.context.add_tool_result("runtime_error", error_message)
            self.context.add_message("assistant", error_message)
            return {
                "success": False,
                "result": error_message,
                "error_code": "AGENT_RUNTIME_FAILED",
                "retriable": True,
            }

    def _process_loop(self) -> str:
        turns = 0

        while turns < self.max_turns:
            turns += 1
            messages = self.context.get_messages()
            tools = self.tools.get_function_defs() if len(self.tools.list_tools()) > 0 else None

            response = self.llm.generate(messages, tools=tools)
            message = response.get("message", {})

            if message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    self._execute_tool_call(tool_call)
                continue

            content = message.get("content", "")
            if content:
                logger.info("Received final response from LLM")
                return content

            raise RuntimeError("LLM returned no text response")

        raise RuntimeError("Reached max turns in agent runtime")

    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> None:
        function = tool_call.get("function", {})
        tool_name = function.get("name")
        arguments = function.get("arguments", {})

        logger.info(f"Executing tool: {tool_name}")
        try:
            result = self.tools.execute(tool_name, **arguments)
            self.context.add_tool_result(tool_name, result)
            logger.info(f"Tool {tool_name} completed successfully")
        except Exception as exc:
            error_msg = f"Error executing {tool_name}: {exc}"
            self.context.add_tool_result(tool_name, error_msg)
            logger.error(error_msg)

    def get_context_stats(self) -> Dict[str, Any]:
        return self.context.get_stats()

    def clear_context(self) -> None:
        self.context.clear()
