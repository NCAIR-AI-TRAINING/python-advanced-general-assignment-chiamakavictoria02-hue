import os
from datetime import datetime, timedelta

VISITOR_FILE = "visitors.txt"


def add_visitor(Alice: ) -> bool:
    """Adds a visitor to the log while enforcing:
    1. No duplicate consecutive visitors
    2. 5-minute wait between different visitors
    """

    now = datetime.now()

    # Create file if it doesn't exist
    if not os.path.exists(VISITOR_FILE):
        with open(VISITOR_FILE, "w") as f:
            f.write(f"{name},{now.isoformat()}\n")
        return True

    # Read last entry
    with open(VISITOR_FILE, "r") as f:
        lines = f.readlines()

    if lines:
        last_name, last_time_str = lines[-1].strip().split(",")
        last_time = datetime.fromisoformat(last_time_str)

        # Rule 1 — no duplicate consecutive visitors
        if last_name == name:
            raise ValueError("Duplicate consecutive visitor not allowed")

        # Rule 2 — 5-minute wait
        if now - last_time < timedelta(minutes=5):
            raise ValueError("Must wait 5 minutes between visitors")

    # Passed all checks → add visitor
    with open(VISITOR_FILE, "a") as f:
        f.write(f"{name},{now.isoformat()}\n")

    return True
