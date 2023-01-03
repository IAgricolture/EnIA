
from src.logic.model.dbConnection import licenze
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
        licenzaTrovata = Licenza()
        licenzaTrovata.id = str(trovato.get("_id"))
        licenzaTrovata.tipo = trovato.get("tipo")
        licenzaTrovata.costo = trovato.get("costo")
        licenzaTrovata.data_attivazione = trovato.get("data_attivazione")
        licenzaTrovata.data_scadenza = trovato.get("data_scadenza")
        licenzaTrovata.scaduta = trovato.get("scaduta")
        return licenzaTrovata
    
    def creaLicenza(licenza : Licenza):
        """
            Questo metodo instanzia una licenza sul database
        """
        licenze.insert_one({
            "tipo" : licenza.tipo,
            "costo" : licenza.costo,
            "data_attivazione" : licenza.data_attivazione,
            "data_scadenza" : licenza.data_scadenza,
            "scaduta" : licenza.scaduta
        })



