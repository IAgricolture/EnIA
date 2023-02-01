

import requests


class OpenMeteoAdapter():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_data(self):
        url = "https://api.open-meteo.com/v1/forecast?"\
            "latitude=" + str(self.lat) + "&longitude=" + str(self.lon) + \
            "&hourly=temperature_2m,relativehumidity_2m,precipitation"
        data = requests.get(url).json()

        return data
