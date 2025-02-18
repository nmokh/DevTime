import unittest
import json
from datetime import datetime
from devtime.storage import task_to_dict, dict_to_task, save_tasks, load_tasks
from devtime.scheduler import Task

class TestStorageFunctions(unittest.TestCase):

    def test_task_to_dict(self):
        task = Task("Test Task", 2, "2025-03-01 18:00", "high", 12345)
        task_dict = task_to_dict(task)

        self.assertEqual(task_dict["name"], "Test Task")
        self.assertEqual(task_dict["duration"], 2)
        self.assertEqual(task_dict["deadline"], "2025-03-01 18:00")
        self.assertEqual(task_dict["priority"], "high")
        self.assertEqual(task_dict["id"], 12345)

    def test_dict_to_task(self):
        task_dict = {
            "name": "Test Task",
            "duration": 2,
            "deadline": "2025-03-01 18:00",
            "priority": "high",
            "id": 12345
        }
        task = dict_to_task(task_dict)

        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.duration, 2)
        self.assertEqual(task.deadline.strftime("%Y-%m-%d %H:%M"), "2025-03-01 18:00")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.id, 12345)

if __name__ == "__main__":
    unittest.main()
