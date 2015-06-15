
import unittest
import httpretty as HP
import json

from malaysiaflights import mas


class MASRequestTests(unittest.TestCase):

    def url_helper(self, from_, to, date):

        host = 'https://flymh.mobi'
        path = "/TravelAPI/travelapi/shop/1/mh/"
        "{from_}/{to}/1/0/0/Economy/{date}/".format(from_=from_,
                                                    to=to, date=date)

        headers = {'X-apiKey': '52e6d6d613d3a3e825ac02253fe6b5a4',
                   'Accept': 'application/json'}

        return host, path, headers

    @HP.activate
    def test_search_calls_api_using_correct_path_and_headers(self):
        host, path, headers = self.url_helper('KUL', 'TGG', '2015-06-15')
        HP.register_uri(HP.GET, host+path, status=200)

        mas.search('KUL', 'TGG', '2015-06-15')
        mocked_request = HP.last_request()

        self.assertEqual(path, mocked_request.path)
        self.assertEqual(headers['X-apiKey'],
                         mocked_request.headers['X-apiKey'])
        self.assertEqual(headers['Accept'],
                         mocked_request.headers['Accept'])


class ResponseExtractionTests(unittest.TestCase):

    def fixture_loader(self, path):
        prefix = 'malaysiaflights/fixtures/'
        with open(prefix + path, 'r') as file_:
            return json.loads(file_.read())

    def setUp(self):
        self.single = self.fixture_loader('mas-single-econ.json')
        self.zero = self.fixture_loader('mas-no-flights.json')

    def test_get_number_of_flights_for_valid_response(self):
        json = self.single
        actual = mas.get_number_of_flights(json)
        self.assertEqual(2, actual)

    def test_get_number_of_flights_for_no_flights_on_date(self):
        json = self.zero
        actual = mas.get_number_of_flights(json)
        self.assertEqual(0, actual)

    def test_get_flight_details_using_index_0_should_return_results(self):
        json = self.single
        expected = {
            'flight_number': 'MH1326',
            'departure_airport': 'KUL',
            'arrival_airport': 'TGG',
            'departure_time': '2015-06-15T07:25:00.000+08:00',
            'arrival_time': '2015-06-15T08:20:00.000+08:00',
            'total_fare': '255.45',
            'fare_currency': 'MYR'}
        actual = mas.get_flight_details(json, 0)
        self.assertEqual(expected, actual)

    def test_get_flight_details_using_index_1_should_return_results(self):
        json = self.single
        expected = {
            'flight_number': 'MH1336',
            'departure_airport': 'KUL',
            'arrival_airport': 'TGG',
            'departure_time': '2015-06-15T14:40:00.000+08:00',
            'arrival_time': '2015-06-15T15:35:00.000+08:00',
            'total_fare': '255.45',
            'fare_currency': 'MYR'}
        actual = mas.get_flight_details(json, 1)
        self.assertEqual(expected, actual)
