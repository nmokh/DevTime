from datetime import datetime
from devtime.config import load_config

class Task:
    """Represents a task with a name, duration, deadline, and priority."""
    
    PRIORITIES = {"low", "medium", "high"}

    def __init__(self, name: str, duration: float, deadline: str, priority: str = "medium", task_id: int = None):
        """
        Initialize a Task instance.

        Args:
            name (str): The name of the task.
            duration (float): The duration of the task in hours.
            deadline (str): The deadline for the task in "YYYY-MM-DD HH:MM" format.
            priority (str): The priority level ("low", "medium", or "high").
            task_id (int, optional): The ID of the task.
        
        Raises:
            ValueError: If the provided priority is not valid.
        """
        if priority not in self.PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Choose from {self.PRIORITIES}")
        
        self.id = task_id if task_id is not None else generate_task_id()
        self.name = name
        self.duration = duration
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M") if isinstance(deadline, str) else deadline
        self.priority = priority

    def __repr__(self):
        return f"Task({self.name}, {self.duration}h, {self.deadline}, {self.priority})"

class WorkSchedule:
    """Represents the work schedule with defined working hours and breaks."""
    
    def __init__(self, day_of_week):
        """
        Initialize a WorkSchedule instance.

        Args:
            day_of_week (str): The day of the week.
        """
        config = load_config()
        work_hours = config["work_hours"].get(day_of_week, {"start": None, "end": None})

        if work_hours["start"] is None or work_hours["end"] is None:
            self.is_day_off = True
        else:
            self.is_day_off = False
            self.start_hour = work_hours["start"]
            self.end_hour = work_hours["end"]
            self.max_concentration_hours = config["max_concentration_hours"]
            self.min_break_minutes = config["min_break_minutes"]

    def get_available_hours(self):
        """
        Calculate the total available working hours in a day considering breaks.

        Returns:
            float: The available working hours.
        """
        total_time = (self.end_hour - self.start_hour) * 60
        work_blocks = total_time // (self.work_block + self.break_time)
        available_hours = work_blocks * (self.work_block / 60)
        return min(available_hours, self.max_daily_hours)

    def __repr__(self):
        return (f"WorkSchedule(Start: {self.start_hour}, End: {self.end_hour}, "
                f"Work Block: {self.work_block} min, Break: {self.break_time} min, "
                f"Max Daily Hours: {self.max_daily_hours})")

def generate_schedule(tasks, schedule):
    """
    Generate an optimal work schedule for the day.

    Args:
        tasks (list[Task]): The list of tasks.
        schedule (WorkSchedule): The work schedule to use for planning.

    Returns:
        tuple: A tuple containing:
            - schedule_plan (list[Task]): Tasks scheduled for today.
            - remaining_tasks (list[Task]): Tasks that could not be scheduled.
    """
    now = datetime.now()
    tasks = [task for task in tasks if task.deadline >= now]

    priority_map = {"low": 3, "medium": 2, "high": 1}
    tasks.sort(key=lambda t: (t.deadline, priority_map[t.priority]))

    available_hours = schedule.get_available_hours()
    schedule_plan = []
    used_hours = 0
    remaining_tasks = []

    for task in tasks:
        if used_hours + task.duration <= available_hours:
            schedule_plan.append(task)
            used_hours += task.duration
        else:
            remaining_tasks.append(task)

    return schedule_plan, remaining_tasks