"""
Ollama LLM wrapper for ai-system.

Provides a simple chat interface with optional tool definitions.
"""

import logging
import requests
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class OllamaLLM:
    """Ollama LLM interface for chat and tool execution."""

    def __init__(
        self,
        model: str = "llama3.3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        timeout: int = 60,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout
        logger.info(f"Initialized OllamaLLM: {self.model} @ {self.base_url}")

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": self.temperature},
        }

        if tools:
            payload["tools"] = tools

        logger.debug(f"Sending request to Ollama chat: {len(messages)} messages")

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()

        result = response.json()
        logger.debug("Received response from Ollama")
        return result

    def supports_tools(self) -> bool:
        return True
