from src.logic.model.DatiMeteo import DatiMeteo
from src.dbConnection import datimeteo
from bson.objectid import ObjectId

class DatiMeteoDAO():
    def creaDatiMeteo( datiMeteo : DatiMeteo) -> str:
        """Questo metodo crea un'istanza di dati meteo sul database

        Args:
            datiMeteo (DatiMeteo): oggetto dati meteo che verrà istanziato sul database
        Returns:
            str: id dei dati meteo appena generati
        """
        result = datimeteo.insert_one({
            "nome" : datiMeteo.nome,
            "aqi" : datiMeteo.aqi,
            "no2" : datiMeteo.no2,
            "estremo" : datiMeteo.estremo,
            "pm10" : datiMeteo.pm10,
            "pm25" : datiMeteo.pm25,
            "o3" : datiMeteo.o3,
            "data_rilevazione" : datiMeteo.data_rilevazione,
            "terreno" : datiMeteo.terreno
        })
        return str(result.inserted_id)
    def findDatiMeteo(id : str) -> DatiMeteo:
        """Questo metodo restituisce i dati meteo trovati sul database
           tramite id
        Args:
            id (str): ObjectId dei dati meteo

        Returns:
            DatiMeteo: datiMeteo trovati dal database
        """
        trovato = datimeteo.find_one({"_id" : ObjectId(id)})
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        aqi = trovato.get("aqi")
        no2 = trovato.get("no2")
        estremo = trovato.get("estremo")
        pm10 = trovato.get("pm10")
        pm25 = trovato.get("pm25")
        o3 = trovato.get("o3")
        data_rilevazione = trovato.get("data_rilevazione")
        terreno = trovato.get("terreno")
        datiMeteoTrovati = DatiMeteo(nome, data_rilevazione, estremo, aqi, pm10, pm25, o3, no2, terreno)
        return datiMeteoTrovati