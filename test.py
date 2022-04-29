import unittest
from calculator import *


class TestParse(unittest.TestCase):

    def test_parse_num(self):
        self.assertEqual(parse(['8']), ['8'])

    def test_parse_normal(self):
        self.assertEqual(parse(['-2', '+', '4', '-', '5', '+', '6']),
                         ['-2', '+', '4', '-', '5', '+', '6'])

    def test_parse_multiple(self):
        self.assertEqual(parse(['9', '+++', '10', '--', '8']),
                         ['9', '+', '10', '+', '8'])


class TestCharsToNumbers(unittest.TestCase):

    def test_to_num_num(self):
        self.assertEqual(chars_to_numbers(['8']), [8])

    def test_to_num_normal(self):
        self.assertEqual(
            chars_to_numbers(['-2', '+', '4', '-', '5', '+', '6']),
            [-2, 4, -5, 6])

    def test_to_num_multiple(self):
        self.assertEqual(chars_to_numbers(['9', '+', '10', '+', '8']),
                         [9, 10, 8])


if __name__ == '__main__':
    unittest.main()
