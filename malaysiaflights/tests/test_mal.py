
import unittest
import datetime
import httpretty as HP
import json

from malaysiaflights.malindo import Malindo as Mal


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

        Mal.initialise_api_call()
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
                'DepartureDate': '/Date(' + Mal.to_api(date) + ')/',
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
        d = datetime.datetime(2015, 6, 25)
        host, path, headers, body = self.search_url_helper('TGG', 'SZB',
                                                           d, 'key')
        HP.register_uri(HP.POST, host+path, status=200)

        Mal.search_api('TGG', 'SZB', d, 'key')
        mocked_request = HP.last_request()
        actual_body = json.loads(mocked_request.body.decode())

        self.assertEqual(path, mocked_request.path)

        self.assertEqual(headers['Content-Type'],
                         mocked_request.headers['Content-Type'])

        self.assertEqual(headers['WscContext'],
                         mocked_request.headers['WscContext'])

        self.assertEqual(body, actual_body)


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
        actual = Mal.get_number_of_results(json)
        self.assertEqual(3, actual)

    def test_get_number_of_results_for_no_flights_on_date(self):
        json = self.zero
        actual = Mal.get_number_of_results(json)
        self.assertEqual(0, actual)

    def test_get_flight_details_using_index_0_should_return_results(self):
        json = self.single
        expected = {
            'flight_number': 'OD1164',
            'departure_airport': 'SZB',
            'arrival_airport': 'PEN',
            'departure_time': '/Date(1435966800000+0800)/',
            'arrival_time': '/Date(1435970400000+0800)/',
            'total_fare': 48.75,
            'fare_currency': 'MYR'}
        actual = Mal.get_direct_flight_details(json, 0)
        self.assertEqual(expected, actual)

    def test_get_flight_details_using_index_1_should_return_results(self):
        json = self.single
        expected = {
            'flight_number': 'OD1170',
            'departure_airport': 'SZB',
            'arrival_airport': 'PEN',
            'departure_time': '/Date(1435987200000+0800)/',
            'arrival_time': '/Date(1435990800000+0800)/',
            'total_fare': 83.75,
            'fare_currency': 'MYR'}
        actual = Mal.get_direct_flight_details(json, 1)
        self.assertEqual(expected, actual)

    def test_is_connecting_flights_should_return_true_for_connecting(self):
        json = self.connecting
        actual = Mal.is_connecting_flights(json, 0)
        self.assertTrue(actual)

    def test_is_connecting_flights_should_return_false_for_direct(self):
        json = self.single
        actual = Mal.is_connecting_flights(json, 1)
        self.assertFalse(actual)

    def test_get_connecting_flights_details_return_results(self):
        json = self.connecting
        expected = {
            'flight_number': 'OD2101 + OD1004',
            'departure_airport': 'PEN',
            'arrival_airport': 'BKI',
            'departure_time': '/Date(1435974300000+0800)/',
            'arrival_time': '/Date(1435994400000+0800)/',
            'total_fare': 583.95,
            'fare_currency': 'MYR'}
        actual = Mal.get_connecting_flight_details(json, 0)
        self.assertEqual(expected, actual)


class TimeConversionTest(unittest.TestCase):

    def test_get_utc_timestamp_returns_correct_timestamp(self):
        date_object = datetime.datetime(2015, 10, 21)
        expected = '1445385600000'
        actual = Mal.to_api(date_object)
        self.assertEqual(expected, actual)

    def test_get_utc_timestamp_returns_13_digits_string(self):
        date_object = datetime.datetime(2015, 10, 21)
        expected = 13
        actual = len(Mal.to_api(date_object))
        self.assertEqual(expected, actual)

    def test_convert_extracted_time_to_datetime_returns_correct_object(self):
        offset = datetime.timedelta(hours=8)
        expected = datetime.datetime(2015, 7, 4, 13, 20,
                                     tzinfo=datetime.timezone(offset))
        actual = Mal.to_datetime('/Date(1435987200000+0800)/')
        self.assertEqual(expected, actual)
