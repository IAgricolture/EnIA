from src.logic.model.DatiInquinamento import DatiInquinamento
from src.dbConnection import datiinqui
from bson.objectid import ObjectId

class DatiInquinamentoDAO():
    def creaDatiInquinamento( datiinquinamento : DatiInquinamento) -> str:
        """Questo metodo crea un'istanza di dati inquinamento sul database

        Args:
            datiinquinamento (DatiInquinamento): oggetto dati inquinamento che verrà istanziato sul database
        Returns:
            str: id dei dati inquinamento appena generati
        """
        result = datiinqui.insert_one({
            "nome" : datiinquinamento.nome,
            "aqi" : datiinquinamento.aqi,
            "no2" : datiinquinamento.no2,
            "estremo" : datiinquinamento.estremo,
            "pm10" : datiinquinamento.pm10,
            "pm25" : datiinquinamento.pm25,
            "o3" : datiinquinamento.o3,
            "data_rilevazione" : datiinquinamento.data_rilevazione,
            "terreno" : datiinquinamento.terreno
        })

        return str(result.inserted_id)

    def findDatiInquinamento(id : str) -> DatiInquinamento:
        """Questo metodo restituisce i dati inquinamento trovati sul database
           tramite id
        Args:
            id (str): ObjectId dei dati inquinamento

        Returns:
            Datiinquinamento: datiinquinamento trovati dal database
        """
        trovato = datiinqui.find_one({"_id" : ObjectId(id)})
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
        datiInquinamentoTrovati = DatiInquinamento(nome, data_rilevazione, estremo, aqi, pm10, pm25, o3, no2, terreno)

        return datiInquinamentoTrovati