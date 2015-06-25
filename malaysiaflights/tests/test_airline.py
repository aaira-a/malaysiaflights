
import unittest
import datetime

from malaysiaflights.airline import Airline as A


class TimeFormatTests(unittest.TestCase):

    def test_convert_to_datetime_returns_correct_object(self):
        expected = datetime.datetime(2015, 8, 31)
        actual = A.convert_to_datetime('2015-08-31')
        self.assertEqual(expected, actual)
