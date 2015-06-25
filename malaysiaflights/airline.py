
import datetime


class Airline(object):

    def convert_to_datetime(date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")
