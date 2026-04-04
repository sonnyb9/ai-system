"""
Tool abstraction for ai-system.

Defines the base Tool interface and a ToolRegistry for managing
available tools in a safe, extensible way.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class Tool(ABC):
    """Base class for all ai-system tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def to_function_def(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __repr__(self) -> str:
        return f"<Tool: {self.name}>"


class ToolRegistry:
    """Registry for available tools."""

    def __init__(
        self,
        safe_dir: Optional[str] = None,
        approval_callback: Optional[Callable[[str, Dict[str, Any]], bool]] = None,
    ):
        self._tools: Dict[str, Tool] = {}
        self.safe_dir = safe_dir
        self.approval_callback = approval_callback
        logger.info("Tool registry initialized")

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def get_function_defs(self) -> List[Dict[str, Any]]:
        return [tool.to_function_def() for tool in self._tools.values()]

    def execute(self, name: str, **kwargs) -> Any:
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")

        logger.info(f"Executing tool: {name}")
        if self.approval_callback and self._needs_approval(name, kwargs):
            approved = self.approval_callback(name, kwargs)
            if not approved:
                return "❌ Operation cancelled (approval denied)"

        return tool.execute(**kwargs)

    def _needs_approval(self, tool_name: str, params: Dict[str, Any]) -> bool:
        return False
