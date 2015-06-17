
import requests


def search(from_, to, date):

    url = 'https://argon.airasia.com/api/7.0/search'

    data = {'origin': from_,
            'destination': to,
            'depart': date,
            'passenger-count': '1',
            'infant-count': '0',
            'currency': 'MYR'}

    return requests.post(url, data=data)
