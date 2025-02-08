import json
from datetime import datetime
from devtime.scheduler import Task

TASKS_FILE = "tasks.json"         # File to store tasks
SCHEDULES_FILE = "schedules.json"   # File to store schedule history

def task_to_dict(task):
    """
    Convert a Task object to a dictionary with the deadline in ISO format.

    Args:
        task (Task): The task to convert.

    Returns:
        dict: Dictionary representation of the task.
    """
    return {
        "name": task.name,
        "duration": task.duration,
        "deadline": task.deadline.isoformat(),
        "priority": task.priority
    }

def schedule_to_dict(schedule_date, tasks):
    """
    Convert a schedule to a dictionary for JSON storage.

    Args:
        schedule_date (datetime): The date of the schedule.
        tasks (list[Task]): List of tasks in the schedule.

    Returns:
        dict: Dictionary representation of the schedule.
    """
    return {
        "date": schedule_date.strftime("%Y-%m-%d"),
        "tasks": [task_to_dict(task) for task in tasks]
    }

def dict_to_task(data):
    """
    Convert a dictionary to a Task object, parsing the deadline from an ISO string.

    Args:
        data (dict): Dictionary representation of a task.

    Returns:
        Task: The corresponding Task object.
    """
    deadline_str = data["deadline"]

    # If the deadline is already a datetime object, format it as a string
    if isinstance(deadline_str, datetime):
        return Task(data["name"], data["duration"], deadline_str.strftime("%Y-%m-%d %H:%M"), data["priority"])

    # Convert the ISO formatted string to a datetime object
    try:
        # Replace 'T' with a space if present
        deadline_str = deadline_str.replace("T", " ")
        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

    return Task(
        name=data["name"],
        duration=data["duration"],
        deadline=deadline_dt.strftime("%Y-%m-%d %H:%M"),
        priority=data["priority"]
    )

def save_tasks(tasks):
    """
    Save a list of tasks to the tasks JSON file.

    Args:
        tasks (list[Task]): The tasks to save.
    """
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump([task_to_dict(task) for task in tasks], f, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def save_schedule(schedule_date, tasks):
    """
    Save a schedule by appending a new entry to the schedule history.

    Args:
        schedule_date (datetime): The date of the schedule.
        tasks (list[Task]): The tasks included in the schedule.
    """
    schedule_data = {
        "date": schedule_date.strftime("%Y-%m-%d"),
        "tasks": [task_to_dict(task) for task in tasks]
    }

    # Load existing schedules
    schedules = load_schedules()
    schedules.append(schedule_data)

    try:
        with open(SCHEDULES_FILE, "w") as f:
            json.dump(schedules, f, indent=4)
    except IOError as e:
        print(f"Error saving schedule: {e}")

def load_tasks():
    """
    Load tasks from the tasks JSON file and convert them into Task objects.

    Returns:
        list[Task]: List of tasks.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            return [dict_to_task(d) for d in data]
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠ Warning: tasks.json is empty or corrupted. Resetting task list.")
        return []

def load_schedules():
    """
    Load the list of saved schedules from the schedules JSON file.

    Returns:
        list: List of schedules.
    """
    try:
        with open(SCHEDULES_FILE, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: JSON file is corrupted. Resetting schedule list.")
        return []