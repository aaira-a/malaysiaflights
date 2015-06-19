
import unittest
import httpretty as HP
from bs4 import BeautifulSoup as BS
from urllib.parse import parse_qsl

from malaysiaflights import firefly


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

        firefly.search('TGG', 'SZB', '27/06/2015')
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
        json = self.single
        actual = firefly.get_number_of_results(json)
        self.assertEqual(5, actual)

    def test_get_number_of_results_for_no_flights_on_date(self):
        json = self.zero
        actual = firefly.get_number_of_results(json)
        self.assertEqual(0, actual)
