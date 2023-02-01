from datetime import datetime
import requests


class SenseSquareAdapter:
    # prendi attributi opzionali start_date, end_date, start_time, end_time
    def __init__(self, nazione, regione, provincia, comune,
                 start_date=None, end_date=None, formato="json"):
        currentdate = str(datetime.now()).split(" ")
        date = currentdate[0]
        precisehour = currentdate[1].split(":")
        time = precisehour[0] + ":" + precisehour[1]
        self.date = date
        self.time = time
        self.nazione = nazione
        self.regione = regione
        self.provincia = provincia
        self.comune = comune
        self.start_date = start_date
        self.end_date = end_date
        self.formato = formato

    def get_data_for_today(self):
        url = "https://square.sensesquare.eu:5001/placeView"
        body = {
            "apikey": "3BK3D0LWE8DQ",  # Codice API, NON MODIFICARE
            "tempo": "giorno",
            "date": self.date,
            "time": self.time,
            "nazione": self.nazione,
            "regione": self.regione,
            "provincia": self.provincia,
            "comune": self.comune,
            "zoom": "3",  # 0 per tutte le nazioni, 1 per tutte le regioni, 2 per tutte le province, 3 per tutti i comuni, 4 NON VA
            "predictions": "true",  # NON TOCCARE
            "fonti": "[]"  # NON TOCCARE
        }
        return requests.post(url=url, data=body).json()

    def get_data_time_interval(self):
        # se gli attributi opzionali sono none lancia eccezione
        if self.start_date is None or self.end_date is None:
            raise Exception("Missing optional attributes")
        url = "https://square.sensesquare.eu:5001/download"
        body = {
            "apikey": "3BK3D0LWE8DQ",
            "req_type": "daily",
            "zoom": "3",
            "start_date": self.start_date,  # Formato deve essere YYYY-MM-DD
            "start_hour": "0",
            "end_date": self.end_date,
            "end_hour": "0",
            "nazione": self.nazione,
            "regione": self.regione,
            "provincia": self.provincia,
            "comune": self.comune,
            "format": self.formato
        }
        datiapi = requests.post(url=url, data=body).text
        print("formato" + self.formato)
        # Multipli oggetti JSON, ne faccio un parse decente in un array di
        # oggetti json.
        if (self.formato == "json"):
            arrayDati = datiapi.split("\n")  # Ne ottengo un array
            # Rimuovo un elemento vuoto creato con lo split, all'ultimo posto
            arrayDati.pop(len(arrayDati) - 1)
            return arrayDati
        else:
            return datiapi  # Qualsiasi altro formato, è buono così com'è.
