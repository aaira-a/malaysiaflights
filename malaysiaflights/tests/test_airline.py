
import unittest
import datetime
import httpretty as HP
import re
from unittest import mock

from malaysiaflights.airline import Airline as A
from malaysiaflights.mas import MAS


class TimeFormatTests(unittest.TestCase):

    def test_convert_to_datetime_returns_correct_object(self):
        expected = datetime.datetime(2015, 8, 31)
        actual = A.convert_to_datetime('2015-08-31')
        self.assertEqual(expected, actual)


class AirlineMainTest(unittest.TestCase):

    def setUp(self):
        self.date = datetime.datetime(2015, 7, 14)

    @mock.patch('requests.get')
    def test_main_returns_empty_if_error_in_request(self, mock_request):
        results = MAS().main('TGG', 'KUL', self.date)
        self.assertEqual([], results)

    @HP.activate
    def test_main_returns_empty_if_info_is_unextractable(self):
        HP.register_uri(HP.GET, re.compile('[\s\S]'), body={"error"})
        results = MAS().main('TGG', 'KUL', self.date)
        self.assertEqual([], results)
