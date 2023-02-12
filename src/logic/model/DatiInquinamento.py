
import datetime


class DatiInquinamento():
    def __init__(self, nome: str, data_rilevazione: datetime, estremo: bool,
                 aqi: int, pm10: int, pm25: int, o3: int, no2: int, terreno: str, id=0):
        self.nome = nome
        self.data_rilevazione = data_rilevazione
        self.estremo = estremo
        self.aqi = aqi
        self.pm10 = pm10
        self.pm25 = pm25
        self.o3 = o3
        self.no2 = no2
        self.terreno = terreno
        self.id = id
