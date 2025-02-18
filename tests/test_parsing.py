import unittest
from datetime import datetime
from devtime.cli import parse_date, parse_priority

class TestParsingFunctions(unittest.TestCase):

    def test_parse_priority_numeric(self):
        self.assertEqual(parse_priority("1"), "high")
        self.assertEqual(parse_priority("2"), "medium")
        self.assertEqual(parse_priority("3"), "low")

    def test_parse_priority_text(self):
        self.assertEqual(parse_priority("high"), "high")
        self.assertEqual(parse_priority("medium"), "medium")
        self.assertEqual(parse_priority("low"), "low")
        self.assertEqual(parse_priority("unknown"), "medium")  # За замовчуванням "medium"

    def test_parse_date_only_time(self):
        now = datetime.now()
        result = parse_date("15:00")
        expected_date = now.strftime("%Y-%m-%d")
        self.assertEqual(result.strftime("%Y-%m-%d %H:%M"), f"{expected_date} 15:00")

    def test_parse_date_full_format(self):
        result = parse_date("2025-03-01 15:00")
        self.assertEqual(result.strftime("%Y-%m-%d %H:%M"), "2025-03-01 15:00")

if __name__ == "__main__":
    unittest.main()
