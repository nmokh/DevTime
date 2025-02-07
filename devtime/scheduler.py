from datetime import datetime

class Task:
    PRIORITIES = {"low", "medium", "high"}

    def __init__(self, name: str, duration: int, deadline: str, priority: str = "medium"):
        if priority not in self.PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Choose from {self.PRIORITIES}")
        
        self.name = name
        self.duration = duration
        
        # Перетворюємо строку у datetime
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        else:
            self.deadline = deadline  # Якщо вже datetime, залишаємо як є

        self.priority = priority

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

    # Фільтруємо тільки актуальні завдання
    now = datetime.now()
    tasks = [task for task in tasks if task.deadline >= now]

    # Словник для пріоритетів (чим менше число, тим вищий пріоритет)
    priority_map = {"low": 3, "medium": 2, "high": 1}

    # Сортуємо завдання за дедлайном і пріоритетом
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
            remaining_tasks.append(task)  # Переносимо на наступний день

    return schedule_plan, remaining_tasks