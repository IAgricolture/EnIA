
from src.dbConnection import licenze
from src.logic.model.Licenza import Licenza
from flask import jsonify
from bson.objectid import ObjectId

class LicenzaDAO():

    def findLicenza(id : str) -> Licenza:
        """
            Questo metodo trova una licenza sul database, usando il suo ObjectId
            :return: Licenza
        """
        trovato = licenze.find_one({"_id" : ObjectId(id)})
        
        id = str(trovato.get("_id"))
        tipo = trovato.get("tipo")
        costo = trovato.get("costo")
        data_attivazione = trovato.get("data_attivazione")
        data_scadenza = trovato.get("data_scadenza")
        scaduta = trovato.get("scaduta")
        proprietario = trovato.get("proprietario")

        licenzaTrovata = Licenza(id, tipo, costo, data_attivazione, data_scadenza, scaduta, proprietario)

        return licenzaTrovata
    
    def creaLicenza(licenza : Licenza) -> str:
        """
            Questo metodo instanzia una licenza sul database
        """
        result = licenze.insert_one({
            "tipo" : licenza.tipo,
            "costo" : licenza.costo,
            "data_attivazione" : licenza.data_attivazione,
            "data_scadenza" : licenza.data_scadenza,
            "scaduta" : licenza.scaduta,
            "proprietario" : licenza.proprietario
        })

        return str(result.inserted_id)




