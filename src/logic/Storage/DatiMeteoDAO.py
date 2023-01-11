from src.logic.model.DatiMeteo import DatiMeteo
from src.dbConnection import datimeteo
from bson.objectid import ObjectId

class DatiMeteoDAO():
    def creaDatiMeteo(datiMeteo : DatiMeteo) -> str:
        """Questo metodo crea un'istanza di dati meteo sul database
           con un oggetto DatiMeteo dato in input

        Args:
            datiMeteo (DatiMeteo): Oggetto contentente i dati meteo

        Returns:
            str: id dell'istanza dati_meteo sul database appena creata
        """
        result = datimeteo.insert_one({
            "nome" : datiMeteo.nome,
            "data_rilevazione" : datiMeteo.data_rilevazione,
            "estremo" : datiMeteo.data_rilevazione,
            "pressione" : datiMeteo.pressione,
            "umidità" : datiMeteo.umidità,
            "temperatura" : datiMeteo.temperatura,
            "vento_direzione" : datiMeteo.vento_direzione,
            "vento_intensità" : datiMeteo.vento_intensità,
            "terreno" : datiMeteo.terreno
        })
        return str(result.inserted_id)

    def trovaDatiMeteo(str : id) -> DatiMeteo:
        """Questo metodo restituisce i dati meteo trovati sul database
           tramite id

        Args:
            str (id): ObjectId dei dati meteo

        Returns:
            DatiMeteo: dati meteo trovati sul database
        """
        trovato = datimeteo.find_one({"_id" : ObjectId(id)})
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        data_rilevazione = trovato.get("data_rilevazione")
        estremo = trovato.get("estremo")
        pressione = trovato.get("pressione")
        umidità = trovato.get("umidità")
        temperatura = trovato.get("temperatura")
        vento_direzione = trovato.get("vento_direzione")
        vento_intensità = trovato.get("vento_intensità")
        terreno = trovato.get("terreno")
        datiMeteoTrovati = DatiMeteo(nome, data_rilevazione, estremo, pressione, umidità, temperatura, vento_direzione, vento_intensità, terreno)
        return datiMeteoTrovati