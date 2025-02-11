import json
from datetime import datetime
from devtime.scheduler import Task

TASKS_FILE = "tasks.json"  # File to store tasks
SCHEDULES_FILE = "schedules.json"  # File to store schedule history
COMPLETED_TASKS_FILE = "completed_tasks.json"  # File to store completed tasks

def task_to_dict(task):
    """
    Converts a Task object to a dictionary with the deadline in ISO format.

    Args:
        task (Task): The task to convert.

    Returns:
        dict: Dictionary representation of the task.
    """
    return {
        "name": task.name,
        "duration": task.duration,
        "deadline": task.deadline.strftime("%Y-%m-%d %H:%M") if isinstance(task.deadline, datetime) else task.deadline,
        "priority": task.priority,
        "id": task.id
    }

def schedule_to_dict(schedule_date, tasks):
    """
    Converts a schedule to a dictionary for JSON storage.

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
    Converts a dictionary to a Task object, parsing the deadline from an ISO string.

    Args:
        data (dict): Dictionary representation of a task.

    Returns:
        Task: The corresponding Task object.
    """
    deadline_str = data.get("deadline")

    if deadline_str is None:
        deadline_dt = None
    elif isinstance(deadline_str, datetime):
        deadline_dt = deadline_str
    else:
        try:
            deadline_str = deadline_str.replace("T", " ")
            deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

    return Task(
        name=data["name"],
        duration=data["duration"],
        deadline=deadline_dt.strftime("%Y-%m-%d %H:%M") if deadline_dt else None,
        priority=data["priority"],
        task_id=data.get("id")
    )

def save_tasks(tasks):
    """
    Saves a list of tasks to the tasks JSON file.

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
    Saves a schedule by appending a new entry to the schedule history.

    Args:
        schedule_date (datetime): The date of the schedule.
        tasks (list[Task]): The tasks included in the schedule.
    """
    schedule_data = {
        "date": schedule_date.strftime("%Y-%m-%d"),
        "tasks": [task_to_dict(task) for task in tasks]
    }

    schedules = load_schedules()
    schedules.append(schedule_data)

    try:
        with open(SCHEDULES_FILE, "w") as f:
            json.dump(schedules, f, indent=4)
    except IOError as e:
        print(f"Error saving schedule: {e}")

def save_completed_tasks(tasks):
    """
    Saves the list of completed tasks to a JSON file.

    Args:
        tasks (list[Task]): List of completed tasks.
    """
    with open(COMPLETED_TASKS_FILE, "w") as f:
        json.dump([task_to_dict(task) for task in tasks], f, indent=4)

def load_tasks():
    """
    Loads tasks from the tasks JSON file and converts them into Task objects.

    Returns:
        list[Task]: List of tasks.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            tasks = [dict_to_task(d) for d in data]
            assign_task_ids(tasks)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠ Warning: tasks.json is empty or corrupted. Resetting task list.")
        return []

def load_schedules():
    """
    Loads the list of saved schedules from the schedules JSON file.

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

def load_completed_tasks():
    """
    Loads completed tasks from the completed tasks JSON file.

    Returns:
        list[Task]: List of completed tasks.
    """
    try:
        with open(COMPLETED_TASKS_FILE, "r") as f:
            data = json.load(f)
            return [dict_to_task(d) for d in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

import random

def generate_task_id():
    """Generates a unique 5-digit numeric ID for a task.

    Returns:
        int: A unique 5-digit task ID.
    """
    existing_ids = {task.id for task in load_tasks()}  # All existing task IDs
    while True:
        new_id = random.randint(10000, 99999)  # Generate a 5-digit ID
        if new_id not in existing_ids:
            return new_id

def assign_task_ids(tasks):
    """
    Assigns unique numerical IDs to tasks in order of their addition.
    
    Args:
        tasks (list): List of Task objects.
    """
    existing_ids = {task.id for task in tasks if task.id is not None}
    
    for task in tasks:
        if task.id is None: 
            task.id = generate_task_id()