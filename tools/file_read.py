"""
File read tool for ai-system.

Provides a safe read-only file access tool for the agent runtime.
"""

import logging
from pathlib import Path
from typing import Any, Dict

from tools.base import Tool

logger = logging.getLogger(__name__)


class FileReadTool(Tool):
    """Tool that reads a text file from the configured safe directory."""

    def __init__(self, safe_dir: str = None):
        self.safe_dir = Path(safe_dir).resolve() if safe_dir else None

    @property
    def name(self) -> str:
        return "file_read"

    @property
    def description(self) -> str:
        return "Read the contents of a text file within the safe directory."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute path to the file to read."
                }
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        if not path:
            raise ValueError("path is required")

        resolved_path = Path(path)
        if not resolved_path.is_absolute():
            if self.safe_dir is None:
                raise ValueError("Safe directory is not configured for file_read")
            resolved_path = self.safe_dir / path

        resolved_path = resolved_path.resolve()
        if self.safe_dir:
            try:
                resolved_path.relative_to(self.safe_dir)
            except ValueError:
                raise ValueError(f"Path '{path}' is outside safe directory '{self.safe_dir}'")

        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found: {resolved_path}")
        if not resolved_path.is_file():
            raise ValueError(f"Path is not a file: {resolved_path}")

        logger.info(f"Reading file: {resolved_path}")
        return resolved_path.read_text(encoding="utf-8")
