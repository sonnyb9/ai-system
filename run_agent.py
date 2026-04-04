import json
from controller.agent_controller import AgentController
from tools.logger import log
from config import TASK_QUEUE

def load_queue():
    try:
        with open(TASK_QUEUE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log(f"Error loading task queue: {e}")
        return []

def save_queue(tasks):
    try:
        with open(TASK_QUEUE, "w") as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        log(f"Error saving task queue: {e}")

def main():
    controller = AgentController(str(TASK_QUEUE.parent.parent))  # Pass base dir

    tasks = load_queue()
    if not tasks:
        log("No tasks in queue")
        return

    remaining = []

    for task in tasks:
        task_result = controller.run_task(task)
        if task_result["success"]:
            log(f"Task completed: {task_result['result'][:80]}")
        else:
            log(f"Task failed: {task_result['error_code']}")
            if task_result.get("retriable", False):
                remaining.append(task)
            else:
                log("Task not retriable, discarding")

    save_queue(remaining)
    log(f"Processed {len(tasks)} tasks, {len(remaining)} remaining")

if __name__ == "__main__":
    main()

