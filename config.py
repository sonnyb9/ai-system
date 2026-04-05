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

# Runtime configuration defaults
# Default to tinyllama for low-memory systems, override with AI_SYSTEM_MODEL env var
# For tool calling, use llama3.1:8b or newer (requires ~4GB RAM)
MODEL = os.getenv("AI_SYSTEM_MODEL", "tinyllama:latest")
OLLAMA_URL = os.getenv("AI_SYSTEM_OLLAMA_URL", "http://localhost:11434")
TEMPERATURE = float(os.getenv("AI_SYSTEM_TEMPERATURE", "0.7"))
TIMEOUT = int(os.getenv("AI_SYSTEM_TIMEOUT", "60"))
MAX_TURNS = int(os.getenv("AI_SYSTEM_MAX_TURNS", "10"))
CONTEXT_WINDOW = int(os.getenv("AI_SYSTEM_CONTEXT_WINDOW", "20"))
TOKEN_BUDGET = int(os.getenv("AI_SYSTEM_TOKEN_BUDGET", "8000"))
SAFE_DIR = os.getenv("AI_SYSTEM_SAFE_DIR")

# Call on import
ensure_directories()