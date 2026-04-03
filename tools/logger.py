import os

def log(message):
    # Determine the directory of this file (tools/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, "logs", "agent.log")

    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a") as f:
        f.write(message + "\n")
