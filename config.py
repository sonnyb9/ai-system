"""
Centralized configuration for the AI System.
Handles paths, environment variables, and settings in a cross-platform way.
"""

import os
from pathlib import Path

# Base directory - use environment variable or default to parent of this file
BASE_DIR = Path(os.getenv("AI_SYSTEM_ROOT", Path(__file__).parent))

# Core paths
TASK_QUEUE = BASE_DIR / "tasks" / "task_queue.json"
SCHEDULED_TASKS = BASE_DIR / "tasks" / "scheduled_tasks.json"
LOG_FILE = BASE_DIR / "logs" / "agent.log"
PROVIDERS_DIR = BASE_DIR / "providers"
ROUTING_FILE = BASE_DIR / "routing" / "routing.json"
SCHEMAS_DIR = BASE_DIR / "schemas"

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        BASE_DIR / "tasks",
        BASE_DIR / "logs",
        BASE_DIR / "providers",
        BASE_DIR / "routing",
        BASE_DIR / "schemas"
    ]
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)

# Call on import
ensure_directories()