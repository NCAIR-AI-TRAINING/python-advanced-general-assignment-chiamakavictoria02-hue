import os
from datetime import datetime, timedelta

LOG_FILE = "visitors.txt"


class DuplicateVisitorError(Exception):
    """Raised when the same visitor appears consecutively."""
    pass


class WaitTimeError(Exception):
    """Raised when a visitor arrives before the mandatory wait time."""
    pass


def log_visitor(name: str):
    """Logs a visitor if rules are met:
    - No duplicate consecutive visitors
    - 5-minute wait between different visitors
    """

    name = name.strip()

    # If file does not exist, create it and log immediately
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{name},{timestamp}\n")
        return "Visitor logged (file created)."

    # File exists → read the last entry
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        # File exists but empty
        with open(LOG_FILE, "w") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{name},{timestamp}\n")
        return "Visitor logged."

    # Parse the last visitor log
    last_line = lines[-1].strip()
    last_name, last_time_str = last_line.split(",")
    last_time = datetime.fromisoformat(last_time_str)

    # Rule 1: Prevent duplicate consecutive visitors
    if name.lower() == last_name.lower():
        raise DuplicateVisitorError("Duplicate consecutive visitor detected!")

    # Rule 2: Enforce 5-minute wait
    now = datetime.now()
    if now - last_time < timedelta(minutes=5):
        minutes_left = 5 - (now - last_time).seconds // 60
        raise WaitTimeError(
            f"Please wait at least 5 minutes before the next visitor. Try again in {minutes_left} minute(s)."
        )

    # Passed all checks → append visitor log
    with open(LOG_FILE, "a") as f:
        timestamp = now.isoformat()
        f.write(f"{name},{timestamp}\n")

    return "Visitor logged successfully."


# Running directly
if __name__ == "__main__":
    try:
        visitor = input("Enter visitor name: ").strip()
        message = log_visitor(visitor)
        print(message)
    except (DuplicateVisitorError, WaitTimeError) as e:
        print("Error:", e)
    except Exception as ex:
        print("Unexpected error:", ex)