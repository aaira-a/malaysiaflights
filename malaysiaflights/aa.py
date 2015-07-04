
import dateutil.parser
import requests

from malaysiaflights.airline import Airline


class AirAsia(Airline):

    @staticmethod
    def search(from_, to, date):

        url = 'https://argon.airasia.com/api/7.0/search'

        data = {'origin': from_,
                'destination': to,
                'depart': AirAsia.format_input(date),
                'passenger-count': '1',
                'infant-count': '0',
                'currency': 'MYR'}

        return requests.post(url, data=data)

    @staticmethod
    def get_number_of_results(json):
        try:
            date = next(iter(json['depart']))
            return len(json['depart'][date]['details']['low-fare'])
        except:
            return 0

    @staticmethod
    def is_connecting_flights(json, index):
        date = next(iter(json['depart']))
        j = json['depart'][date]['details']['low-fare'][index]
        number_of_flights = len(j['segments'])
        number_of_stopovers = int(j['number-of-stops'])

        return bool(number_of_flights and number_of_stopovers)

    @staticmethod
    def get_direct_flight_details(json, index):
        date = next(iter(json['depart']))
        j = json['depart'][date]['details']['low-fare'][index]['segments'][0]
        fare = json['depart'][date]['details']['low-fare'][index]

        flight_details = {
            'flight_number': ''.join(j['flight-number'].split()),
            'departure_airport': j['origincode'],
            'arrival_airport': j['destinationcode'],
            'departure_time': j['departure-datetime'],
            'arrival_time': j['arrival-datetime'],
            'total_fare': fare['total']['adult'],
            'fare_currency': fare['currency'],
            }

        return flight_details

    @staticmethod
    def format_input(datetime):
        return datetime.strftime("%d-%m-%Y")

    @staticmethod
    def format_output(output):
        return dateutil.parser.parse(output)
