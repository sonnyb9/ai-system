"""
Conversation context manager for ai-system.

Tracks message history, token budget, and tool results.
"""

import logging
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ContextManager:
    """Manage conversation history and context state."""

    def __init__(
        self,
        max_messages: int = 20,
        token_budget: int = 8000,
        system_prompt: Optional[str] = None,
    ):
        self.max_messages = max_messages
        self.token_budget = token_budget
        self.system_prompt = system_prompt
        self._messages: deque = deque(maxlen=max_messages)
        logger.info(f"Context manager initialized (max_messages={max_messages})")

    def add_message(self, role: str, content: str, **metadata) -> None:
        message: Dict[str, Any] = {"role": role, "content": content}
        if metadata:
            message.update(metadata)
        self._messages.append(message)
        logger.debug(f"Added {role} message ({len(content)} chars)")

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        content = f"Tool '{tool_name}' result:\n{str(result)}"
        self.add_message("tool", content, name=tool_name)

    def get_messages(self) -> List[Dict[str, Any]]:
        messages: List[Dict[str, Any]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(list(self._messages))
        return messages

    def get_last_message(self) -> Optional[Dict[str, Any]]:
        return self._messages[-1] if self._messages else None

    def clear(self) -> None:
        self._messages.clear()
        logger.info("Context cleared")

    def prune_old_messages(self, keep_last: int = 10) -> int:
        if len(self._messages) <= keep_last:
            return 0
        removed = len(self._messages) - keep_last
        self._messages = deque(list(self._messages)[-keep_last:], maxlen=self.max_messages)
        logger.info(f"Pruned {removed} old messages")
        return removed

    def estimate_tokens(self) -> int:
        total_chars = len(self.system_prompt or "")
        for msg in self._messages:
            total_chars += len(msg["content"])
        return total_chars // 4

    def is_over_budget(self) -> bool:
        return self.estimate_tokens() > self.token_budget

    def get_stats(self) -> Dict[str, Any]:
        return {
            "message_count": len(self._messages),
            "max_messages": self.max_messages,
            "estimated_tokens": self.estimate_tokens(),
            "token_budget": self.token_budget,
            "over_budget": self.is_over_budget(),
            "has_system_prompt": bool(self.system_prompt),
        }

    def __len__(self) -> int:
        return len(self._messages)

    def __repr__(self) -> str:
        return f"<ContextManager: {len(self._messages)} messages, ~{self.estimate_tokens()} tokens>"
