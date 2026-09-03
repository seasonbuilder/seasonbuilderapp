import unittest

from coach_edge_config import parse_bool_parameter


class CoachEdgeConfigTests(unittest.TestCase):
    def test_true_values_are_case_insensitive(self):
        for value in ("true", "TRUE", "Yes", "1", "on"):
            with self.subTest(value=value):
                self.assertTrue(parse_bool_parameter(value))

    def test_false_values_are_case_insensitive(self):
        for value in ("false", "FALSE", "No", "0", "off"):
            with self.subTest(value=value):
                self.assertFalse(parse_bool_parameter(value, default=True))

    def test_missing_or_invalid_value_uses_launcher_default(self):
        self.assertTrue(parse_bool_parameter(None, default=True))
        self.assertFalse(parse_bool_parameter("unexpected", default=False))


if __name__ == "__main__":
    unittest.main()
