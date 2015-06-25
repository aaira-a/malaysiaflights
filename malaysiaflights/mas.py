
import requests

from malaysiaflights.airline import Airline


class MAS(Airline):

    def search(from_, to, date):
        date = MAS.format_input(date)

        url = "https://flymh.mobi/TravelAPI/travelapi/shop/1/mh/"
        "{from_}/{to}/1/0/0/Economy/{date}/".format(from_=from_,
                                                    to=to, date=date)

        headers = {'X-apiKey': '52e6d6d613d3a3e825ac02253fe6b5a4',
                   'Accept': 'application/json'}

        return requests.get(url, headers=headers)

    def get_number_of_results(json):
        try:
            return len(json['outboundOptions'])
        except:
            return 0

    def is_connecting_flights(json, index):
        j = json['outboundOptions'][index]
        number_of_flights = len(j['flights'])
        number_of_stopovers = len(j['stopOvers'])

        return bool(number_of_flights and number_of_stopovers)

    def get_direct_flight_details(json, index):
        j = json['outboundOptions'][index]['flights'][0]
        fare = json['outboundOptions'][index]['fareDetails']

        flight_details = {
            'flight_number': j['marketingAirline'] + j['flightNumber'],
            'departure_airport': j['departureAirport']['code'],
            'arrival_airport': j['arrivalAirport']['code'],
            'departure_time': j['depScheduled'],
            'arrival_time': j['arrScheduled'],
            'total_fare': fare['totalTripFare'],
            'fare_currency': fare['fareCurrency'],
            }

        return flight_details

    def get_connecting_flight_details(json, index):
        j = json['outboundOptions'][index]['flights']
        fare = json['outboundOptions'][index]['fareDetails']
        first_flight = 0
        final_flight = len(j)-1

        flight_number = []
        for flight in j:
            flight_number.append(flight['marketingAirline'] +
                                 flight['flightNumber'])

        flight_details = {
            'flight_number': " + ".join(flight_number),
            'departure_airport': j[first_flight]['departureAirport']['code'],
            'arrival_airport': j[final_flight]['arrivalAirport']['code'],
            'departure_time': j[first_flight]['depScheduled'],
            'arrival_time': j[final_flight]['arrScheduled'],
            'total_fare': fare['totalTripFare'],
            'fare_currency': fare['fareCurrency'],
            }

        return flight_details

    def format_input(datetime):
        return datetime.strftime("%Y-%m-%d")
