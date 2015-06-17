
import unittest
import httpretty as HP
import json
from urllib.parse import parse_qsl

from malaysiaflights import aa


class AARequestTests(unittest.TestCase):

    def url_helper(self, from_, to, date):

        host = 'https://argon.airasia.com'
        path = '/api/7.0/search'

        body = {'origin': from_,
                'destination': to,
                'depart': date,
                'passenger-count': '1',
                'infant-count': '0',
                'currency': 'MYR'}

        return host, path, body

    @HP.activate
    def test_search_calls_api_using_correct_path_and_body(self):
        host, path, body = self.url_helper('KUL', 'TGG', '18-06-2015')
        HP.register_uri(HP.POST, host+path, status=200)

        aa.search('KUL', 'TGG', '18-06-2015')
        mocked_request = HP.last_request()
        actual_body = dict(parse_qsl(mocked_request.body.decode()))

        self.assertEqual(path, mocked_request.path)
        self.assertEqual(body, actual_body)


class ResponseExtractionTests(unittest.TestCase):

    def fixture_loader(self, path):
        prefix = 'malaysiaflights/fixtures/'
        with open(prefix + path, 'r') as file_:
            return json.loads(file_.read())

    def setUp(self):
        self.single = self.fixture_loader('aa-single.json')
        self.zero = self.fixture_loader('aa-no-flights.json')

    def test_get_number_of_results_for_valid_response(self):
        json = self.single
        actual = aa.get_number_of_results(json, '20-06-2015')
        self.assertEqual(4, actual)

    def test_get_number_of_results_for_no_flights_on_date(self):
        json = self.zero
        actual = aa.get_number_of_results(json, '20-06-2015')
        self.assertEqual(0, actual)

    @unittest.skip('no-data-yet')
    def test_is_connecting_flights_should_return_true_for_connecting(self):
        json = ''
        actual = aa.is_connecting_flights(json, '', 0)
        self.assertTrue(actual)

    def test_is_connecting_flights_should_return_false_for_direct(self):
        json = self.single
        actual = aa.is_connecting_flights(json, '20-06-2015', 2)
        self.assertFalse(actual)
