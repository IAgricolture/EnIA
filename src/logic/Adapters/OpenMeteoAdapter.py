

import requests


class OpenMeteoAdapter():
    def __init__(self, lat, lon):
        #controllo latitudine e longitudine
        if lat < -90 or lat > 90:
            raise Exception("Latitudine non valida")
        elif lon < -180 or lon > 180:
            raise Exception("Longitudine non valida")
        self.lat = lat
        self.lon = lon
        
    def get_data(self):
        
        url = "https://api.open-meteo.com/v1/forecast?"\
        "latitude="+str(self.lat)+"&longitude="+str(self.lon)+ "&hourly=temperature_2m,relativehumidity_2m,precipitation"
        data = requests.get(url).json()
        print("dati meteo ------------------------------------------")
        print(data)
        print("fine dati meteo ------------------------------------")
        return data