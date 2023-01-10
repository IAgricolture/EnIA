import datetime
from src.dbConnection import eventi
from src.logic.model.Evento import Evento
from flask import jsonify
from bson.objectid import ObjectId

class EventoDAO():

    def findEvento(id : str) -> Evento:
        """
            Questo metodo trova un Evento sul database, usando il suo ObjectId
            :return: Evento
        """
        trovato = eventi.find_one({"_id" : ObjectId(id)})
        id = str(trovato.get("_id"))
        titolo = str(trovato.get("titolo"))
        descrizione = str(trovato.get("descrizione"))
        orario = trovato.get("orario")
        tipo = str(trovato.get("tipo"))
        azione_umana = bool(trovato.get("azione_umana"))
        visto = bool(trovato.get("visto"))
        eventoTrovato = Evento(id, titolo, descrizione, orario, tipo, azione_umana, visto)
        return eventoTrovato
    
    def creaEvento(evento : Evento) -> str:
        """
            Questo metodo instanzia un evento sul database
        """
        result = eventi.insert_one({
            "titolo" : evento.titolo,
            "descrizione" : evento.descrizione,
            "orario" : evento.orario,
            "tipo" : evento.tipo,
            "azione_umana" : evento.azione_umana,
            "visto" : evento.visto
        })

        return str(result.inserted_id)



