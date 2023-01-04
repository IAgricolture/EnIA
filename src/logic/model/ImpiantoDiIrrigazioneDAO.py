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
        
        id = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        tipo = str(trovato.get("tipo"))
        codice = str(trovato.get("codice"))
        attivo = bool(trovato.get("attivo"))

        impiantoTrovato = ImpiantoDiIrrigazione(id, nome, tipo, codice, attivo)

        return impiantoTrovato
    
    def creaImpianto(impianto : ImpiantoDiIrrigazione) -> str:
        """
            Questo metodo instanzia un impianto di irrigazione sul database
        """
        result = impianti.insert_one({
            "nome" : impianto.nome,
            "tipo" : impianto.tipo,
            "codice" : impianto.codice,
            "attivo" : impianto.attivo
        })
        
        return str(result.inserted_id)




