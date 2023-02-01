import requests


class NominatimAdapter:
    def __init__(self, lat, lon, format, zoom):
        self.lat = lat
        self.lon = lon
        self.format = format
        self.zoom = zoom

    def get_data(self):
        url = f"https://nominatim.openstreetmap.org/reverse?lat={self.lat}&lon={self.lon}&format={self.format}&zoom={self.zoom}"
        response = requests.get(url)
        return response.json()
