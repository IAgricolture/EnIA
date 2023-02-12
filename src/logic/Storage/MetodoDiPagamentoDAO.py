
from src.dbConnection import metodi_di_pagamento
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from flask import jsonify
from bson.objectid import ObjectId


class MetodoDiPagamentoDAO():
    '''
    Classe DAO di Metodi di Pagamento

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    findMetodo(id: str):
        Questo metodo trova un Metodo di pagamento sul database, usando il suo ObjectId
    creaMetodo(metodo: MetodoDiPagamento):
        Questo metodo instanzia un Metodo di pagamento sul database
    findMetodoByProprietario(id: str:        
        Questo metodo trova un Metodo di pagamento sul database, usando l'identificativo del suo proprietario
    modificaMetodo(metodo: MetodoDiPagamento):
        Questo metodo prende in ingresso un oggetto Metodo di pagamento e lo modifica nel database
    '''

    def findMetodo(id: str) -> MetodoDiPagamento:
        '''
        Questo metodo trova un Metodo di pagamento sul database, usando il suo ObjectId

        Parametri
        ----------
        id : str
            id del Metodo

        Returns
        -------
        MetodoTrovato : MetodoDiPagamento
            Restituisce il metodo avente come id quello passto in input
        '''
        
        trovato = metodi_di_pagamento.find_one({"_id": ObjectId(id)})
        id = str(trovato.get("_id"))
        num_carta = str(trovato.get("numero_carta"))
        titolare = str(trovato.get("titolare"))
        scadenza = str(trovato.get("scadenza"))
        cvv = str(trovato.get("cvv"))
        proprietario = str(trovato.get("proprietario"))

        metodoTrovato = MetodoDiPagamento(
            id, num_carta, titolare, scadenza, cvv, proprietario)
        return metodoTrovato

    def creaMetodo(metodo: MetodoDiPagamento) -> str:
        '''
        Questo metodo trova un utente nel database, utilizzando la sua email

        Parametri
        ----------
        metodo : MetodoDiPagamento
            istanza del metodo di Pagamento da memorizzare nel database 

        Returns
        -------
        result : str
            id del metodo di pagamento 
        '''
        
        result = metodi_di_pagamento.insert_one({
            "numero_carta": metodo.num_carta,
            "titolare": metodo.titolare,
            "scadenza": metodo.scadenza,
            "cvv": metodo.cvv,
            "proprietario": metodo.proprietario
        })

        return str(result.inserted_id)

    def findMetodoByProprietario(id: str) -> MetodoDiPagamento:
        '''
        Questo metodo trova un Metodo di pagamento sul database, usando l'identificativo del suo proprietario

        Parametri
        ----------
        id : str
            id del proprietario

        Returns
        -------
        metodoTrovato : MetodoDiPagamento
            Restituisce il netodo avente come id quello passto in input
        '''
        
        trovato = metodi_di_pagamento.find_one({"proprietario": id})
        id = str(trovato.get("_id"))
        num_carta = str(trovato.get("numero_carta"))
        titolare = str(trovato.get("titolare"))
        scadenza = str(trovato.get("scadenza"))
        cvv = str(trovato.get("cvv"))
        proprietario = str(trovato.get("proprietario"))

        metodoTrovato = MetodoDiPagamento(
            id, num_carta, titolare, scadenza, cvv, proprietario)
        return metodoTrovato

    def modificaMetodo(metodo: MetodoDiPagamento):
        '''
        Questo metodo prende in ingresso un oggetto Metodo di pagamento e lo modifica nel database

        Parametri
        ----------
        metodo : MetodoDiPagamento
            istanza del Metodo Di Pagamento da modificare

        Returns
        -------
        None : NoneType
            Restituisce None in caso non e stata effettuata alcuna modifica 
        '''
        
        trovato = MetodoDiPagamentoDAO.findMetodo(metodo.id)
        if (trovato is None):
            return None

        metodi_di_pagamento.update_one({"_id": ObjectId(trovato.id)},
                                       {"$set": {
                                           "numero_carta": metodo.num_carta,
                                           "titolare": metodo.titolare,
                                           "scadenza": metodo.scadenza,
                                           "cvv": metodo.cvv,
                                       }})

        
    def eliminaMetodo(id : str)->bool:
        '''
            Questo metodo prende in ingresso un id ed elimina
             il corrispondente metodo dal database
        '''
            
        result = metodi_di_pagamento.delete_one({"_id": ObjectId(id)})
        if(result.deleted_count == 1):
            return True
        else:
            return False
