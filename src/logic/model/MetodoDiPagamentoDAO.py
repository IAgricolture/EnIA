
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
        id = str(trovato.get("_id"))
        num_carta = str(trovato.get("numero_carta"))
        titolare = str(trovato.get("titolare"))
        scadenza = str(trovato.get("scadenza"))
        cvv = str(trovato.get("cvv"))
        proprietario = str(trovato.get("proprietario"))

        metodoTrovato = MetodoDiPagamento(id, num_carta, titolare, scadenza, cvv, proprietario)
        return metodoTrovato
    
    def creaMetodo(metodo : MetodoDiPagamento) -> str:
        """
            Questo metodo instanzia un Metodo si pagamento sul database
        """
        result = metodi_di_pagamento.insert_one({
            "numero_carta" : metodo.num_carta,
            "titolare" : metodo.titolare,
            "scadenza" : metodo.scadenza,
            "cvv" : metodo.cvv,
            "proprietario" : metodo.proprietario
        })

        return str(result.inserted_id)

    def findMetodoByProprietario(id : str) -> MetodoDiPagamento:
        """
            Questo metodo trova un Metodo di pagamento sul database, usando l'identificativo del suo proprietario
            :return: MetodoDiPagamento
        """
        trovato = metodi_di_pagamento.find_one({"proprietario" : id})
        id = str(trovato.get("_id"))
        num_carta = str(trovato.get("numero_carta"))
        titolare = str(trovato.get("titolare"))
        scadenza = str(trovato.get("scadenza"))
        cvv = str(trovato.get("cvv"))
        proprietario = str(trovato.get("proprietario"))

        metodoTrovato = MetodoDiPagamento(id, num_carta, titolare, scadenza, cvv, proprietario)
        return metodoTrovato


    def modificaMetodo(metodo : MetodoDiPagamento): 
        """
            Questo metodo prende in ingresso un oggetto Metodo di pagamento e lo modifica nel database
        """  
        trovato = MetodoDiPagamentoDAO.findMetodo(metodo.id)
        if(trovato == None):
            return None

        metodi_di_pagamento.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "numero_carta" : metodo.num_carta,
            "titolare": metodo.titolare,
            "scadenza": metodo.scadenza,
            "cvv": metodo.cvv,
        }})