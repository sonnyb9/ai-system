"""
System info tool for ai-system.

Provides runtime environment metadata and system diagnostics.
"""

import datetime
import getpass
import os
import platform
import socket
from typing import Any, Dict

from tools.base import Tool


class SystemInfoTool(Tool):
    """Tool that returns information about the current system."""

    @property
    def name(self) -> str:
        return "system_info"

    @property
    def description(self) -> str:
        return "Return information about the current system environment."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    def execute(self) -> str:
        info = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "cwd": os.getcwd(),
            "environment": {
                "path": os.environ.get("PATH", ""),
                "shell": os.environ.get("SHELL", ""),
                "term": os.environ.get("TERM", ""),
            },
        }

        lines = [f"{key}: {value}" for key, value in info.items() if key != "environment"]
        lines.append("environment:")
        for env_key, env_value in info["environment"].items():
            lines.append(f"  {env_key}: {env_value}")

        return "\n".join(lines)
