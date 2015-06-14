
import requests


def get_flight(from_, to, date):

    url = "https://flymh.mobi/TravelAPI/travelapi/shop/1/mh/"
    "{from_}/{to}/1/0/0/Economy/{date}/".format(from_=from_, to=to, date=date)

    headers = {'X-apiKey': '52e6d6d613d3a3e825ac02253fe6b5a4',
               'Accept': 'application/json'}

    return requests.get(url, headers=headers)


def get_number_of_flights(json):
    try:
        return len(json['outboundOptions'])
    except:
        return 0
