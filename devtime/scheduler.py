from datetime import datetime, timedelta
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
    """Represents the work schedule with defined working hours, lunch, concentration limits, and breaks."""
    
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
            return
        self.is_day_off = False
        self.start_hour = work_hours["start"]
        self.end_hour = work_hours["end"]
        self.lunch_start = config.get("lunch_start", 12)
        self.lunch_end = config.get("lunch_end", 13)
        self.max_concentration_hours = config["max_concentration_hours"]
        self.min_break_minutes = config["min_break_minutes"]

    def is_working_day(self, date):
        """Checks if a given date is a working day based on configuration."""
        weekday = date.strftime("%A")
        work_hours = load_config()["work_hours"].get(weekday, {"start": None, "end": None})
        return work_hours["start"] is not None and work_hours["end"] is not None

    def get_next_working_day(self, date, max_days=7):
        """
        Finds the next working day to avoid infinite loops.

        Args:
            date (datetime): Starting date.
            max_days (int): Maximum days to search.

        Returns:
            datetime: The next working day.

        Raises:
            RuntimeError: If no working day is found within max_days.
        """
        for _ in range(max_days):
            if self.is_working_day(date):
                return date
            date += timedelta(days=1)
        raise RuntimeError(f"No working day found within {max_days} days. Stuck on {date}.")

    def __repr__(self):
        return (f"WorkSchedule(Start: {self.start_hour}, End: {self.end_hour}, "
                f"Max Concentration: {self.max_concentration_hours}h, "
                f"Break: {self.min_break_minutes} min, "
                f"Lunch: {self.lunch_start}:00 - {self.lunch_end}:00)")

def generate_schedule(tasks, initial_schedule):
    """
    Generates a multi-day work schedule based on user configuration.

    Args:
        tasks (list[Task]): List of tasks to schedule.
        initial_schedule (WorkSchedule): Unused here (MVP version).

    Returns:
        tuple: (schedule_plan, remaining_tasks)
    """
    schedule_plan = {}
    now = datetime.now()
    remaining_tasks = [task for task in tasks if task.deadline is None or task.deadline >= now]
    current_day = now.date()
    max_days = 30
    day_counter = 0

    while remaining_tasks and day_counter < max_days:
        day_counter += 1
        day_str = current_day.strftime("%Y-%m-%d")
        weekday = current_day.strftime("%A")
        ws = WorkSchedule(weekday)

        if ws.is_day_off:
            current_day += timedelta(days=1)
            continue

        # Start the day from the current time if the day has already started
        if current_day == now.date():
            now_float = now.hour + now.minute / 60.0
            work_start = max(ws.start_hour, now_float)
        else:
            work_start = ws.start_hour
        work_end = ws.end_hour

        available_blocks = []
        current_time = work_start

        # Form work blocks with breaks
        while current_time < work_end:
            block_end = min(current_time + ws.max_concentration_hours, work_end)
            available_blocks.append((current_time, block_end))
            
            # Add a break after each block if there is space
            break_start = block_end
            break_end = min(block_end + ws.min_break_minutes / 60.0, work_end)
            if break_start < break_end:
                available_blocks.append(("Break", break_start, break_end))
            
            current_time = break_end

        daily_schedule = []
        
        for block in available_blocks:
            if block[0] == "Break":
                daily_schedule.append(("Break", block[1], block[2]))
                continue
            
            block_start, block_end = block
            current_slot = block_start

            while current_slot < block_end and remaining_tasks:
                task = remaining_tasks[0]
                session_time = min(task.duration, block_end - current_slot)
                
                scheduled_start = current_slot
                scheduled_end = current_slot + session_time
                daily_schedule.append((task, scheduled_start, scheduled_end))
                
                current_slot = scheduled_end
                task.duration -= session_time

                if task.duration <= 0:
                    remaining_tasks.pop(0)

        schedule_plan[day_str] = daily_schedule
        current_day += timedelta(days=1)

    if day_counter >= max_days:
        print("Reached maximum day limit while scheduling.")

    return schedule_plan, remaining_tasks
