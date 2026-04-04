import datetime
from config import LOG_FILE

def log(message):
    """Log a message with timestamp to the configured log file."""
    try:
        timestamp = datetime.datetime.now().isoformat()
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} {message}\n")
    except Exception as e:
        # Fallback to print if logging fails
        print(f"LOG ERROR: {e} - {message}")

