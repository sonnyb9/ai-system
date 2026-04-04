"""
File write tool for ai-system.

Provides safe file write access to the agent runtime, restricted to the configured safe directory.
"""

import logging
from pathlib import Path
from typing import Any, Dict

from tools.base import Tool

logger = logging.getLogger(__name__)


class FileWriteTool(Tool):
    """Tool that writes content to a file under the safe directory."""

    def __init__(self, safe_dir: str = None):
        self.safe_dir = Path(safe_dir).resolve() if safe_dir else None

    @property
    def name(self) -> str:
        return "file_write"

    @property
    def description(self) -> str:
        return "Write content to a file within the safe directory."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute path to the file to write."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file."
                }
            },
            "required": ["path", "content"],
        }

    def execute(self, path: str, content: str) -> str:
        if not path:
            raise ValueError("path is required")
        if content is None:
            raise ValueError("content is required")

        resolved_path = Path(path)
        if not resolved_path.is_absolute():
            if self.safe_dir is None:
                raise ValueError("Safe directory is not configured for file_write")
            resolved_path = self.safe_dir / path

        resolved_path = resolved_path.resolve()
        if self.safe_dir:
            try:
                resolved_path.relative_to(self.safe_dir)
            except ValueError:
                raise ValueError(f"Path '{path}' is outside safe directory '{self.safe_dir}'")

        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Writing file: {resolved_path}")
        resolved_path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content.encode('utf-8'))} bytes to {resolved_path}"
