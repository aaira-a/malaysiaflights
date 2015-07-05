
import datetime


class Airline(object):

    def __init__(self):
        pass

    def main(self, from_, to, date):
        results = []

        try:
            response = self.search(from_, to, date)
            data = self.preprocess(response)
            number_of_results = self.get_number_of_results(data)
        except:
            pass

        try:
            for flight in range(0, number_of_results):
                if self.is_connecting_flights(data, flight):
                    result = self.get_connecting_flight_details(data, flight)
                else:
                    result = self.get_direct_flight_details(data, flight)
                results.append(result)
        except:
            pass

        return results

    def convert_to_datetime(date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")

    def preprocess(self, response):
        return response.json()

    def to_representation(date):
        return date.strftime("%I:%M %p")
