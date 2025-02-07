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
        """Returns a string representation of the task"""
        return f"Task({self.name}, {self.duration}h, {self.deadline}, {self.priority})"