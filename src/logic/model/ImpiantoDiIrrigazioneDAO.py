from src.dbConnection import impianti
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from flask import jsonify
from bson.objectid import ObjectId

class ImpiantoDiIrrigazioneDAO():

    def findImpianto(id : str) -> ImpiantoDiIrrigazione:
        """
            Questo metodo trova un Impianto di irrigazione sul database, usando il suo ObjectId
            :return: ImpiantoDiIrrigazione
        """
        trovato = impianti.find_one({"_id" : ObjectId(id)})
        impiantoTrovato = ImpiantoDiIrrigazione()
        impiantoTrovato.id = str(trovato.get("_id"))
        impiantoTrovato.nome = str(trovato.get("nome"))
        impiantoTrovato.tipo = str(trovato.get("tipo"))
        impiantoTrovato.codice = str(trovato.get("codice"))
        impiantoTrovato.attivo = bool(trovato.get("attivo"))
        return impiantoTrovato
    
    def creaImpianto(impianto : ImpiantoDiIrrigazione):
        """
            Questo metodo instanzia un impianto di irrigazione sul database
        """
        impianti.insert_one({
            "nome" : impianto.nome,
            "tipo" : impianto.tipo,
            "codice" : impianto.codice,
            "attivo" : impianto.attivo
        })



