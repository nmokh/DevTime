from datetime import datetime

class Task:
    PRIORITIES = {"low", "medium", "high"}  # Allowed priority levels

    def __init__(self, name: str, duration: int, deadline: str, priority: str = "medium"):
        if priority not in self.PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Choose from {self.PRIORITIES}")
        
        self.name = name  # Task name
        self.duration = duration  # Task duration in hours
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")  # Convert deadline string to datetime
        self.priority = priority  # Task priority (low, medium, high)

    def __repr__(self):
        return f"Task({self.name}, {self.duration}h, {self.deadline}, {self.priority})"

class WorkSchedule:
    def __init__(self, start_hour=9, end_hour=18, work_block=90, break_time=15, max_daily_hours=8):
        """Initialize work schedule with working hours, work blocks, break time, and max daily work hours."""
        self.start_hour = start_hour  # Start of the workday (hour in 24-hour format)
        self.end_hour = end_hour  # End of the workday (hour in 24-hour format)
        self.work_block = work_block  # Duration of a single work block in minutes
        self.break_time = break_time  # Break duration between work blocks in minutes
        self.max_daily_hours = max_daily_hours  # Maximum working hours per day

    def get_available_hours(self):
        """Calculate the total available working hours in a day considering breaks."""
        total_time = (self.end_hour - self.start_hour) * 60  # Total available time in minutes
        work_blocks = total_time // (self.work_block + self.break_time)  # Number of full work blocks in a day
        available_hours = work_blocks * (self.work_block / 60)  # Convert work time to hours
        return min(available_hours, self.max_daily_hours)  # Limit to max daily hours

    def __repr__(self):
        return (f"WorkSchedule(Start: {self.start_hour}, End: {self.end_hour}, "
                f"Work Block: {self.work_block} min, Break: {self.break_time} min, "
                f"Max Daily Hours: {self.max_daily_hours})")

def generate_schedule(tasks, schedule):
    """Generates an optimal work schedule for the day."""
    
    # Filter only current tasks (those that are not overdue)
    now = datetime.now()
    tasks = [task for task in tasks if task.deadline >= now]

    # Sort tasks by deadline and priority
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
            remaining_tasks.append(task)  # Postpone it to the next day

    return schedule_plan, remaining_tasks