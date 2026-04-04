import json
from tools.logger import log
from config import TASK_QUEUE, SCHEDULED_TASKS

def load_json(path):
    """Load JSON from file, return empty list on error."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log(f"Error loading {path}: {e}")
        return []

def save_json(path, data):
    """Save data as JSON to file."""
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"Error saving to {path}: {e}")

def ingest_tasks():
    """Move scheduled tasks to the task queue."""
    scheduled = load_json(SCHEDULED_TASKS)
    if not scheduled:
        log("No scheduled tasks to ingest")
        return

    queue = load_json(TASK_QUEUE)
    queue.extend(scheduled)

    save_json(TASK_QUEUE, queue)
    save_json(SCHEDULED_TASKS, [])

    log(f"Ingested {len(scheduled)} tasks")

if __name__ == "__main__":
    ingest_tasks()

