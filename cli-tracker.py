#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime, timezone

TASK_FILE = "tasks.json"
VALID_STATUSES = {"todo", "in-progress", "done"}

def current_time():
"""Return the current UTC time in ISO 8601 format."""
return datetime.now(timezone.utc).isoformat()

def load_tasks():
"""Load tasks from the JSON file."""
if not os.path.exists(TASK_FILE):
return []

try:
    with open(TASK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        print("Error: tasks.json must contain a JSON array.")
        sys.exit(1)

    return data

except json.JSONDecodeError:
    print("Error: tasks.json contains invalid JSON.")
    sys.exit(1)
except OSError as error:
    print(f"Error reading {TASK_FILE}: {error}")
    sys.exit(1)


def save_tasks(tasks):
"""Save tasks to the JSON file."""
try:
with open(TASK_FILE, "w", encoding="utf-8") as file:
json.dump(tasks, file, indent=2)
file.write("\n")
except OSError as error:
print(f"Error writing {TASK_FILE}: {error}")
sys.exit(1)

def get_next_id(tasks):
"""Return the next available task ID."""
if not tasks:
return 1

return max(task["id"] for task in tasks) + 1


def find_task(tasks, task_id):
"""Find a task by ID."""
for task in tasks:
if task["id"] == task_id:
return task

return None


def parse_task_id(value):
"""Convert a command-line task ID to an integer."""
try:
task_id = int(value)

    if task_id <= 0:
        raise ValueError

    return task_id

except ValueError:
    print("Error: task ID must be a positive integer.")
    sys.exit(1)


def add_task(description):
"""Add a new task."""
description = description.strip()

if not description:
    print("Error: task description cannot be empty.")
    sys.exit(1)

tasks = load_tasks()
now = current_time()

task = {
    "id": get_next_id(tasks),
    "description": description,
    "status": "todo",
    "createdAt": now,
    "updatedAt": now
}

tasks.append(task)
save_tasks(tasks)

print(f"Task added successfully (ID: {task['id']})")


def update_task(task_id, description):
"""Update an existing task's description."""
description = description.strip()

if not description:
    print("Error: task description cannot be empty.")
    sys.exit(1)

tasks = load_tasks()
task = find_task(tasks, task_id)

if task is None:
    print(f"Error: task with ID {task_id} not found.")
    sys.exit(1)

task["description"] = description
task["updatedAt"] = current_time()

save_tasks(tasks)

print(f"Task {task_id} updated successfully.")


def delete_task(task_id):
"""Delete a task."""
tasks = load_tasks()
task = find_task(tasks, task_id)

if task is None:
    print(f"Error: task with ID {task_id} not found.")
    sys.exit(1)

tasks.remove(task)
save_tasks(tasks)

print(f"Task {task_id} deleted successfully.")


def mark_task(task_id, status):
"""Change a task's status."""
if status not in VALID_STATUSES:
print(f"Error: invalid status '{status}'.")
sys.exit(1)

tasks = load_tasks()
task = find_task(tasks, task_id)

if task is None:
    print(f"Error: task with ID {task_id} not found.")
    sys.exit(1)

task["status"] = status
task["updatedAt"] = current_time()

save_tasks(tasks)

if status == "in-progress":
    print(f"Task {task_id} marked as in progress.")
elif status == "done":
    print(f"Task {task_id} marked as done.")
else:
    print(f"Task {task_id} marked as todo.")


def print_task(task):
"""Print a task in a readable format."""
print(
f"[{task['id']}] "
f"{task['description']} "
f"(status: {task['status']})"
)

def list_tasks(status=None):
"""List all tasks or tasks matching a status."""
tasks = load_tasks()

if status is not None:
    if status == "todo":
        status = "todo"
    elif status == "done":
        status = "done"
    elif status == "in-progress":
        status = "in-progress"
    else:
        print(
            "Error: invalid status. "
            "Use 'done', 'todo', or 'in-progress'."
        )
        sys.exit(1)

    tasks = [task for task in tasks if task["status"] == status]

if not tasks:
    print("No tasks found.")
    return

for task in sorted(tasks, key=lambda item: item["id"]):
    print_task(task)


def print_usage():
"""Print command usage."""
print("""
Task Tracker CLI

Usage:
task-cli add "Task description"
task-cli update <id> "New task description"
task-cli delete <id>
task-cli mark-in-progress <id>
task-cli mark-done <id>
task-cli list
task-cli list done
task-cli list todo
task-cli list in-progress
""")

def main():
"""Parse command-line arguments and execute the requested command."""
args = sys.argv[1:]

if not args:
    print_usage()
    sys.exit(1)

command = args[0]

if command == "add":
    if len(args) != 2:
        print('Usage: task-cli add "Task description"')
        sys.exit(1)

    add_task(args[1])

elif command == "update":
    if len(args) != 3:
        print('Usage: task-cli update <id> "New task description"')
        sys.exit(1)

    task_id = parse_task_id(args[1])
    update_task(task_id, args[2])

elif command == "delete":
    if len(args) != 2:
        print("Usage: task-cli delete <id>")
        sys.exit(1)

    task_id = parse_task_id(args[1])
    delete_task(task_id)

elif command == "mark-in-progress":
    if len(args) != 2:
        print("Usage: task-cli mark-in-progress <id>")
        sys.exit(1)

    task_id = parse_task_id(args[1])
    mark_task(task_id, "in-progress")

elif command == "mark-done":
    if len(args) != 2:
        print("Usage: task-cli mark-done <id>")
        sys.exit(1)

    task_id = parse_task_id(args[1])
    mark_task(task_id, "done")

elif command == "list":
    if len(args) > 2:
        print("Usage: task-cli list [done|todo|in-progress]")
        sys.exit(1)

    status = args[1] if len(args) == 2 else None
    list_tasks(status)

else:
    print(f"Error: unknown command '{command}'.")
    print_usage()
    sys.exit(1)


if name == "main":
main()
