import unittest
from datetime import datetime
from devtime.scheduler import WorkSchedule, generate_schedule, Task

class TestScheduleGeneration(unittest.TestCase):

    def setUp(self):
        # Налаштування тестової конфігурації
        self.ws = WorkSchedule("Monday")
        self.ws.start_hour = 9
        self.ws.end_hour = 17
        self.ws.max_concentration_hours = 1
        self.ws.min_break_minutes = 10

    def test_work_schedule_working_day(self):
        self.assertFalse(self.ws.is_day_off)
        self.assertEqual(self.ws.start_hour, 9)
        self.assertEqual(self.ws.end_hour, 17)

    def test_generate_schedule_basic(self):
        tasks = [
            Task("Task A", 1, "2025-03-01 18:00", "high", 10001),
            Task("Task B", 2, "2025-03-01 18:00", "medium", 10002),
        ]
        schedule_plan, remaining = generate_schedule(tasks, self.ws)

        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str in schedule_plan:
            self.assertTrue(len(schedule_plan[today_str]) > 0)

        self.assertEqual(len(remaining), 0)

if __name__ == "__main__":
    unittest.main()
