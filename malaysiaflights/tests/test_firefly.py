
import unittest
import datetime
import httpretty as HP
from bs4 import BeautifulSoup as BS
from urllib.parse import parse_qsl

from malaysiaflights.firefly import FireFly as FF


class FireflyRequestTests(unittest.TestCase):

    def url_helper(self, from_, to, date):

        host = 'https://m.fireflyz.com.my'
        path = '/Search'

        body = {'type': '2',
                'departure_station': from_,
                'arrival_station': to,
                'departure_date': date,
                'adult': '1'}

        return host, path, body

    @HP.activate
    def test_search_calls_api_using_correct_path_and_body(self):
        host, path, body = self.url_helper('TGG', 'SZB', '27/06/2015')
        HP.register_uri(HP.POST, host+path, status=200)

        d = datetime.datetime(2015, 6, 27)
        FF.search('TGG', 'SZB', d)
        mocked_request = HP.last_request()
        actual_body = dict(parse_qsl(mocked_request.body.decode()))

        self.assertEqual(path, mocked_request.path)
        self.assertEqual(body, actual_body)


class ResponseExtractionTests(unittest.TestCase):

    def fixture_loader(self, path):
        prefix = 'malaysiaflights/fixtures/'
        with open(prefix + path, 'r') as file_:
            return BS(file_, 'html.parser')

    def setUp(self):
        self.single = self.fixture_loader('ff-single.html')
        self.zero = self.fixture_loader('ff-no-flights.html')

    def test_get_number_of_results_for_valid_response(self):
        soup = self.single
        actual = FF.get_number_of_results(soup)
        self.assertEqual(5, actual)

    def test_get_number_of_results_for_no_flights_on_date(self):
        soup = self.zero
        actual = FF.get_number_of_results(soup)
        self.assertEqual(0, actual)

    def test_get_flight_details_using_index_0_should_return_results(self):
        soup = self.single
        expected = {
            'flight_number': 'FY2101',
            'departure_airport': 'TGG',
            'arrival_airport': 'SZB',
            'departure_time': '06/27/2015 08:55',
            'arrival_time': '06/27/2015 09:55',
            'total_fare': '98.58',
            'fare_currency': 'MYR',
            }
        actual = FF.get_direct_flight_details(soup, 0)
        self.assertEqual(expected, actual)

    def test_get_flight_details_using_index_1_should_return_results(self):
        soup = self.single
        expected = {
            'flight_number': 'FY2113',
            'departure_airport': 'TGG',
            'arrival_airport': 'SZB',
            'departure_time': '06/27/2015 11:05',
            'arrival_time': '06/27/2015 12:05',
            'total_fare': '108.58',
            'fare_currency': 'MYR',
            }
        actual = FF.get_direct_flight_details(soup, 1)
        self.assertEqual(expected, actual)

    def test_is_connecting_flights_should_return_false_for_direct(self):
        soup = self.single
        actual = FF.is_connecting_flights(soup, 2)
        self.assertFalse(actual)


class TimeConversionTest(unittest.TestCase):

    def test_convert_to_api_format_returns_correct_output(self):
        date_object = datetime.datetime(2015, 10, 13)
        expected = '13/10/2015'
        actual = FF.format_input(date_object)
        self.assertEqual(expected, actual)
