# visitor_logger.py

import os
from datetime import datetime

# --- Custom Exception ---
class DuplicateVisitorError(Exception):
    """Raised when the visitor is already the last entry in the file."""
    pass

# --- Ensure the file exists ---
def ensure_file(filename="visitors.txt"):
    """Create the file if it does not exist."""
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            pass

# --- Add a visitor ---
def add_visitor(name, filename="visitors.txt"):
    """
    Add a visitor with a timestamp.
    Raises DuplicateVisitorError if the visitor is the same as the last one.
    """
    ensure_file(filename)

    # Read existing visitors
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Check for consecutive duplicate
    if lines:
        last_name, _ = lines[-1].split(",", 1)
        if last_name == name:
            raise DuplicateVisitorError(f"{name} is already the last visitor!")

    # Add new visitor with timestamp
    timestamp = datetime.now().isoformat()
    with open(filename, "a") as f:
        f.write(f"{name},{timestamp}\n")

# --- Predefined visitors to add ---
visitor_names = ["Alice", "Bob", "Charlie", "Alice", "David", "Eve"]

print("Adding visitors...\n")

for name in visitor_names:
    try:
        add_visitor(name)
        print(f"Added visitor: {name}")
    except DuplicateVisitorError as e:
        print(f"Duplicate detected: {e}")

# Show final contents of visitors.txt
print("\nFinal contents of visitors.txt:")
with open("visitors.txt", "r") as f:
    for line in f:
        print(line.strip())
