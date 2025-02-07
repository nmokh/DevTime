import json
from datetime import datetime
from devtime.scheduler import Task

TASKS_FILE = "tasks.json"  # Name of the file where tasks will be stored

def task_to_dict(task):
    """
    Converts a Task object into a dictionary, ensuring datetime is stored as an ISO string.
    """
    return {
        "name": task.name,
        "duration": task.duration,
        "deadline": task.deadline.isoformat(),  # Convert datetime to ISO format
        "priority": task.priority
    }

def dict_to_task(data):
    """
    Converts a dictionary back into a Task object, parsing datetime from an ISO string.
    """
    deadline_str = data["deadline"]
    
    # Check if the deadline is already a datetime object (prevent errors)
    if isinstance(deadline_str, datetime):
        return Task(data["name"], data["duration"], deadline_str.strftime("%Y-%m-%d %H:%M"), data["priority"])

    # Convert from ISO format (JSON serialization)
    try:
        deadline_str = deadline_str.replace("T", " ")  # Convert "2025-02-07T10:00:00" -> "2025-02-07 10:00:00"
        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")  # Handle seconds
    except ValueError:
        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")  # Fallback for no seconds

    return Task(
        name=data["name"],
        duration=data["duration"],
        deadline=deadline_dt.strftime("%Y-%m-%d %H:%M"),  # Convert back to datetime
        priority=data["priority"]
    )

def save_tasks(tasks):
    """
    Saves a list of tasks to a JSON file.
    """
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump([task_to_dict(task) for task in tasks], f, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def load_tasks():
    """
    Loads a list of tasks from a JSON file.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            return [dict_to_task(d) for d in data]
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list
    except json.JSONDecodeError:
        print("Warning: JSON file is corrupted. Resetting task list.")
        return []