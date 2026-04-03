import datetime

def log(message):
    timestamp = datetime.datetime.now().isoformat()
    with open("/ai-system/logs/agent.log", "a") as f:
        f.write(f"{timestamp} {message}\n")

