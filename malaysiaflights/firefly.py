
import requests
import re

from malaysiaflights.airline import Airline


class FireFly(Airline):

    def search(from_, to, date):

        url = 'https://m.fireflyz.com.my/Search'

        data = {'type': '2',
                'departure_station': from_,
                'arrival_station': to,
                'departure_date': FireFly.format_input(date),
                'adult': '1'}

        return requests.post(url, data=data)

    def get_number_of_results(soup):
        try:
            return len(soup.find_all('div', class_='market1'))
        except:
            return 0

    def is_connecting_flights(soup, index):
        return False

    def get_direct_flight_details(soup, index):
        flights = soup.find_all('div', class_='market1')

        raw_info_string = flights[index]['onclick']
        pattern = re.compile(r'(\w{2}~\d{4})~\s~~'
                             '(\w{3})~'
                             '(\d{2}\/\d{2}\/\d{4})\s'
                             '(\d{2}:\d{2})~'
                             '(\w{3})~'
                             '(\d{2}\/\d{2}\/\d{4})\s'
                             '(\d{2}:\d{2})')
        captured = re.search(pattern, raw_info_string).groups()

        fare_container = flights[index].div.table.tr.td \
                                       .find_next_siblings('td')[2]

        fare_string = ''.join(fare_container.get_text().split())
        fare = re.search(r'(\d*.\d*)(\w{3})', fare_string).groups()

        flight_details = {
            'flight_number': captured[0].replace('~', ''),
            'departure_airport': captured[1],
            'arrival_airport': captured[4],
            'departure_time': captured[2] + ' ' + captured[3],
            'arrival_time': captured[5] + ' ' + captured[6],
            'total_fare': fare[0],
            'fare_currency': fare[1],
            }

        return flight_details

    def format_input(datetime):
        return datetime.strftime("%d/%m/%Y")
