import json
from tools.logger import log

TASK_QUEUE = "/home/pi/ai-system/tasks/task_queue.json"
SCHEDULED_TASKS = "/home/pi/ai-system/tasks/scheduled_tasks.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def ingest_tasks():
    scheduled = load_json(SCHEDULED_TASKS)
    if not scheduled:
        return

    queue = load_json(TASK_QUEUE)
    queue.extend(scheduled)

    save_json(TASK_QUEUE, queue)
    save_json(SCHEDULED_TASKS, [])

    log(f"Ingested {len(scheduled)} tasks")

if __name__ == "__main__":
    ingest_tasks()

