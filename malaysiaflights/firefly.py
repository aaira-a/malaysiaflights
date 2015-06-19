
import requests


def search(from_, to, date):

    url = 'https://m.fireflyz.com.my/Search'

    data = {'type': '2',
            'departure_station': from_,
            'arrival_station': to,
            'departure_date': date,
            'adult': '1'}

    return requests.post(url, data=data)


def get_number_of_results(soup):
    try:
        return len(soup.find_all('div', class_='market1'))
    except:
        return 0
