
import unittest
import httpretty as HP
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
                'infant-count': '0'}

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
