
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
    def test_get_flight_calls_api_using_correct_path_and_headers(self):
        host, path, headers = self.url_helper('KUL', 'TGG', '2015-06-15')
        HP.register_uri(HP.GET, host+path, status=200)

        mas.get_flight('KUL', 'TGG', '2015-06-15')

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

    def test_get_number_of_flights_for_valid_response(self):
        data = self.fixture_loader('mas-single-econ.json')
        actual = mas.get_number_of_flights(data)
        self.assertEqual(2, actual)

    def test_get_number_of_flights_for_no_flights_on_date(self):
        data = self.fixture_loader('mas-no-flights.json')
        actual = mas.get_number_of_flights(data)
        self.assertEqual(0, actual)
