import requests


class NominatimAdapter:
    def __init__(self, lat, lon, format, zoom):
        #check lat and lon
        if lat > 90 or lat < -90:
            raise Exception("Latitudine o longitudine non valide")
        if lon > 180 or lon < -180:
            raise Exception("Latitudine o longitudine non valide")
        #format' must be one of: xml, json, jsonv2, geojson, geocodejson"
        if format not in ["xml", "json", "jsonv2", "geojson", "geocodejson"]:
            raise Exception("Formato non valido")
        #zoom must be an integer
        if not isinstance(zoom, int):
            raise Exception("Zoom non valido")
        self.lat = lat
        self.lon = lon
        self.format = format
        self.zoom = zoom

    def get_data(self):
        url = f"https://nominatim.openstreetmap.org/reverse?lat={self.lat}&lon={self.lon}&format={self.format}&zoom={self.zoom}"
        response = requests.get(url)
        return response.json()