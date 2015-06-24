
import datetime
import pytz
import requests


def search(from_, to, date):
    session = initialise_api_call()
    response = search_api(from_, to, date, session)
    return response


def initialise_api_call():
    init_url = ('https://mobileapi.malindoair.com/GQWCF_FlightEngine'
                '/GQDPMobileBookingService.svc/InitializeGQService')

    init_headers = {'Content-Type': 'application/json'}

    init_data = {'B2BID': '0',
                 'UserLoginId': '0',
                 'CustomerUserID': 91,
                 'Language': 'en-GB',
                 'isearchType': '15'}

    r1 = requests.post(init_url, headers=init_headers, json=init_data)
    return r1.headers['wsccontext']


def search_api(from_, to, date, session):
    search_url = ('https://mobileapi.malindoair.com/GQWCF_FlightEngine'
                  '/GQDPMobileBookingService.svc/SearchAirlineFlights')

    search_headers = {'Content-Type': 'application/json',
                      'WscContext': session}

    search_data = {
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
            'DepartureDate': '/Date(' + get_utc_timestamp(date) + ')/',
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

    return requests.post(search_url, headers=search_headers, json=search_data)


def get_utc_timestamp(date):
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    timestamp = d.replace(tzinfo=pytz.utc).timestamp()
    return str(int(timestamp*1000))


def get_number_of_results(json):
    try:
        return len(json['SearchAirlineFlightsResult'])
    except:
        return 0


def is_connecting_flights(json, index):
    number_of_flights = len(json['SearchAirlineFlightsResult']
                                [index]['SegmentInformation'])

    return bool(number_of_flights > 1)


def get_direct_flight_details(json, index):
    j = json['SearchAirlineFlightsResult'][index]['SegmentInformation'][0]
    fare = json['SearchAirlineFlightsResult'][index]

    flight_details = {
        'flight_number': j['MACode'] + j['FlightNo'],
        'departure_airport': j['DepCity'],
        'arrival_airport': j['ArrCity'],
        'departure_time': j['DepartureDate'],
        'arrival_time': j['ArrivalDate'],
        'total_fare': fare['FlightAmount'],
        'fare_currency': fare['Currency'],
        }

    return flight_details


def get_connecting_flight_details(json, index):
    j = json['SearchAirlineFlightsResult'][index]['SegmentInformation']
    fare = json['SearchAirlineFlightsResult'][index]
    first_flight = 0
    final_flight = len(j)-1

    flight_number = []
    for flight in j:
        flight_number.append(flight['MACode'] + flight['FlightNo'])

    flight_details = {
        'flight_number': " + ".join(flight_number),
        'departure_airport': j[first_flight]['DepCity'],
        'arrival_airport': j[final_flight]['ArrCity'],
        'departure_time': j[first_flight]['DepartureDate'],
        'arrival_time': j[final_flight]['ArrivalDate'],
        'total_fare': fare['FlightAmount'],
        'fare_currency': fare['Currency'],
        }

    return flight_details
