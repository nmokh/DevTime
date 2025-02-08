from datetime import datetime

class Task:
    """
    Represents a task with a name, duration, deadline, and priority.
    """
    PRIORITIES = {"low", "medium", "high"}

    def __init__(self, name: str, duration: float, deadline: str, priority: str = "medium", task_id: int = None):
        """
        Initialize a Task instance.

        Args:
            name (str): The name of the task.
            duration (float): The duration of the task in hours.
            deadline (str): The deadline for the task in "YYYY-MM-DD HH:MM" format.
            priority (str): The priority level ("low", "medium", or "high").

        Raises:
            ValueError: If the provided priority is not valid.
        """
        if priority not in self.PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Choose from {self.PRIORITIES}")
        
        self.id = task_id  # Assign task ID

        self.name = name
        self.duration = duration
        
        # Convert deadline string to a datetime object if necessary
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        else:
            self.deadline = deadline

        self.priority = priority

    def __repr__(self):
        return f"Task({self.name}, {self.duration}h, {self.deadline}, {self.priority})"

class WorkSchedule:
    """
    Represents the work schedule with defined working hours, work block duration,
    break time between blocks, and maximum daily working hours.
    """
    def __init__(self, start_hour=9, end_hour=18, work_block=90, break_time=15, max_daily_hours=8):
        """
        Initialize a WorkSchedule instance.

        Args:
            start_hour (int): Start of the workday (24-hour format).
            end_hour (int): End of the workday (24-hour format).
            work_block (int): Duration of one work block in minutes.
            break_time (int): Duration of break between work blocks in minutes.
            max_daily_hours (int): Maximum working hours allowed per day.
        """
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.work_block = work_block
        self.break_time = break_time
        self.max_daily_hours = max_daily_hours

    def get_available_hours(self):
        """
        Calculate the total available working hours in a day considering breaks.

        Returns:
            float: The available working hours.
        """
        total_time = (self.end_hour - self.start_hour) * 60  # Total minutes available
        work_blocks = total_time // (self.work_block + self.break_time)
        available_hours = work_blocks * (self.work_block / 60)  # Convert minutes to hours
        return min(available_hours, self.max_daily_hours)

    def __repr__(self):
        return (f"WorkSchedule(Start: {self.start_hour}, End: {self.end_hour}, "
                f"Work Block: {self.work_block} min, Break: {self.break_time} min, "
                f"Max Daily Hours: {self.max_daily_hours})")

def generate_schedule(tasks, schedule):
    """
    Generates an optimal work schedule for the day.

    Filters out tasks with deadlines in the past, sorts tasks by deadline and priority,
    and assigns tasks until the available working hours are exhausted. Tasks that do not fit
    are postponed.

    Args:
        tasks (list[Task]): The list of tasks.
        schedule (WorkSchedule): The work schedule to use for planning.

    Returns:
        tuple: A tuple containing:
            - schedule_plan (list[Task]): Tasks scheduled for today.
            - remaining_tasks (list[Task]): Tasks that could not be scheduled.
    """
    # Filter out tasks whose deadlines have passed
    now = datetime.now()
    tasks = [task for task in tasks if task.deadline >= now]

    # Priority mapping: lower number means higher priority
    priority_map = {"low": 3, "medium": 2, "high": 1}

    # Sort tasks by deadline and then by priority
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