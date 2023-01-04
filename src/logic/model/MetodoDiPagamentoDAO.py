
from src.dbConnection import metodi_di_pagamento
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from flask import jsonify
from bson.objectid import ObjectId

class MetodoDiPagamentoDAO():

    def findMetodo(id : str) -> MetodoDiPagamento:
        """
            Questo metodo trova un Metodo di pagamento sul database, usando il suo ObjectId
            :return: MetodoDiPagamento
        """
        trovato = metodi_di_pagamento.find_one({"_id" : ObjectId(id)})
        metodoTrovato = MetodoDiPagamento()
        metodoTrovato.id = str(trovato.get("_id"))
        metodoTrovato.num_carta = str(trovato.get("numero_carta"))
        metodoTrovato.titolare = str(trovato.get("titolare"))
        metodoTrovato.scadenza = str(trovato.get("scadenza"))
        metodoTrovato.cvv = str(trovato.get("cvv"))
        
        return metodoTrovato
    
    def creaMetodo(metodo : MetodoDiPagamento):
        """
            Questo metodo instanzia un Metodo si pagamento sul database
        """
        metodi_di_pagamento.insert_one({
            "numero_carta" : metodo.num_carta,
            "titolare" : metodo.titolare,
            "scadenza" : metodo.scadenza,
            "cvv" : metodo.cvv
        })



