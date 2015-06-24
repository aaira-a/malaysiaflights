
import unittest
import httpretty as HP
import json

from malaysiaflights import malindo as mal


class MalRequestTests(unittest.TestCase):

    def init_url_helper(self):

        host = 'https://mobileapi.malindoair.com'
        path = ('/GQWCF_FlightEngine/GQDPMobileBookingService.svc'
                '/InitializeGQService')

        headers = {'Content-Type': 'application/json'}

        body = {'B2BID': '0',
                'UserLoginId': '0',
                'CustomerUserID': 91,
                'Language': 'en-GB',
                'isearchType': '15'}

        return host, path, headers, body

    @HP.activate
    def test_api_initialisation_calls_api_using_correct_syntax(self):
        host, path, headers, body = self.init_url_helper()
        HP.register_uri(HP.POST, host+path, status=200, wsccontext='session')

        mal.initialise_api_call()
        mocked_request = HP.last_request()
        actual_body = json.loads(mocked_request.body.decode())

        self.assertEqual(path, mocked_request.path)

        self.assertEqual(headers['Content-Type'],
                         mocked_request.headers['Content-Type'])

        self.assertEqual(body, actual_body)

    def search_url_helper(self, from_, to, date, session):

        host = 'https://mobileapi.malindoair.com'

        path = ('/GQWCF_FlightEngine/GQDPMobileBookingService.svc'
                '/SearchAirlineFlights')

        headers = {'Content-Type': 'application/json',
                   'WscContext': session}

        body = {
            'sd': {
                'Adults': 1,
                'AirlineCode': '',
                'ArrivalCity': to,
                'ArrivalCityName': 'null',
                'BookingClass': 'null',
                'CabinClass': 0,
                'ChildAge': [],
                'Children': 0,
                'CustomerId': 0,
                'CustomerType': 0,
                'CustomerUserId': 91,
                'DepartureCity': from_,
                'DepartureCityName': 'null',
                'DepartureDate': '/Date(' + mal.get_utc_timestamp(date) + ')/',
                'DepartureDateGap': 0,
                'DirectFlightsOnly': 'false',
                'Infants': 0,
                'IsPackageUpsell': 'false',
                'JourneyType': 1,
                'PreferredCurrency': 'MYR',
                'ReturnDate': '/Date(-2208988800000)/',
                'ReturnDateGap': 0,
                'SearchOption': 1
                },
            'fsc': '0'
            }

        return host, path, headers, body

    @HP.activate
    def test_search_api_calls_api_using_correct_syntax(self):
        host, path, headers, body = self.search_url_helper('TGG', 'SZB',
                                                           '2015-06-25', 'key')
        HP.register_uri(HP.POST, host+path, status=200)

        mal.search_api('TGG', 'SZB', '2015-06-25', 'key')
        mocked_request = HP.last_request()
        actual_body = json.loads(mocked_request.body.decode())

        self.assertEqual(path, mocked_request.path)

        self.assertEqual(headers['Content-Type'],
                         mocked_request.headers['Content-Type'])

        self.assertEqual(headers['WscContext'],
                         mocked_request.headers['WscContext'])

        self.assertEqual(body, actual_body)


class TimestampTests(unittest.TestCase):

    def test_get_utc_timestamp_returns_correct_timestamp(self):
        expected = '1440460800000'
        actual = mal.get_utc_timestamp('2015-08-25')
        self.assertEqual(expected, actual)

    def test_get_utc_timestamp_returns_13_digits_string(self):
        expected = 13
        actual = len(mal.get_utc_timestamp('2015-08-31'))
        self.assertEqual(expected, actual)


class ResponseExtractionTests(unittest.TestCase):

    def fixture_loader(self, path):
        prefix = 'malaysiaflights/fixtures/'
        with open(prefix + path, 'r') as file_:
            return json.loads(file_.read())

    def setUp(self):
        self.single = self.fixture_loader('mal-single.json')
        self.zero = self.fixture_loader('mal-no-flights.json')
        self.connecting = self.fixture_loader('mal-connecting.json')

    def test_get_number_of_results_for_valid_response(self):
        json = self.single
        actual = mal.get_number_of_results(json)
        self.assertEqual(3, actual)

    def test_get_number_of_results_for_no_flights_on_date(self):
        json = self.zero
        actual = mal.get_number_of_results(json)
        self.assertEqual(0, actual)

    def test_is_connecting_flights_should_return_true_for_connecting(self):
        json = self.connecting
        actual = mal.is_connecting_flights(json, 0)
        self.assertTrue(actual)

    def test_is_connecting_flights_should_return_false_for_direct(self):
        json = self.single
        actual = mal.is_connecting_flights(json, 1)
        self.assertFalse(actual)
