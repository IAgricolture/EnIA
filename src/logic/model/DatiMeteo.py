import datetime

class DatiMeteo():
    def __init__(self, nome : str, data_rilevazione : datetime, estremo : bool, pressione : int, umidità : int, temperatura : int, vento_direzione : int, vento_intensità : float,terreno : str, id = 0):
        self.nome = nome
        self.data_rilevazione = data_rilevazione
        self.estremo = estremo
        self.pressione = pressione
        self.umidità = umidità
        self.temperatura = temperatura
        self.vento_direzione = vento_direzione
        self.vento_intensità = vento_intensità
        self.terreno = terreno
        self.id = id