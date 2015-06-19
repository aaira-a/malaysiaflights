
import requests


def search(from_, to, date):

    url = 'https://m.fireflyz.com.my/Search'

    data = {'type': '2',
            'departure_station': from_,
            'arrival_station': to,
            'departure_date': date,
            'adult': '1'}

    return requests.post(url, data=data)
