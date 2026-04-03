import json
from controller.agent_controller import AgentController
from tools.logger import log

TASK_QUEUE = "/home/pi/ai-system/tasks/task_queue.json"

def load_queue():
    with open(TASK_QUEUE, "r") as f:
        return json.load(f)

def save_queue(tasks):
    with open(TASK_QUEUE, "w") as f:
        json.dump(tasks, f, indent=2)

def main():
    controller = AgentController("/home/pi/ai-system")

    tasks = load_queue()
    if not tasks:
        return

    remaining = []

    for task in tasks:
        result = controller.run_task(task)
        if result:
            log(f"Task completed: {result[:80]}")
        else:
            log("Task failed, keeping in queue")
            remaining.append(task)

    save_queue(remaining)

if __name__ == "__main__":
    main()

