# Task Tracker CLI

A simple command-line task tracker built in Python. Tasks are stored locally in a `tasks.json` file. No dependencies, no DB, just the standard library.

## Features

- Add, update, and delete tasks
- Mark tasks as `todo`, `in-progress` or `done`
- List all tasks or filter by status
- Tasks persist between runs in `tasks.json`

## Requirements

- Python 3.7+

## Usage

Clone the repo and run the script directly

```
git clone https://github.com/0xgitpushpray/task-tracker
cd task-tracker
python3 cli-tracker.py <command>
```

## Commands

```
# Add a new task
python3 cli-tracker.py add "Buy groceries"

# Update a task's description
python3 cli-tracker.py update 1 "Buy groceries and cook dinner"

# Delete a task
python3 cli-tracker.py delete 1

# Mark a task as in progress
python3 cli-tracker.py mark-in-progress 1

# Mark a task as done
python3 cli-tracker.py mark-done 1

# List all tasks
python3 cli-tracker.py list

# List tasks by status
python3 cli-tracker.py done
python3 cli-tracker.py todo
python3 cli-tracker.py in-progress
```

## How it works

Each task is stored as a JSON object with an `id`, `description`, `status`, `createdAt`, and `updatedAt` timestamp. All tasks live in `tasks.json`, created automatically in the working directory on first use.
