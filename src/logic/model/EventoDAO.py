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
        eventoTrovato = Evento()
        eventoTrovato.id = str(trovato.get("_id"))
        eventoTrovato.titolo = str(trovato.get("titolo"))
        eventoTrovato.descrizione = str(trovato.get("descrizione"))
        eventoTrovato.orario = trovato.get("orario")
        eventoTrovato.tipo = str(trovato.get("tipo"))
        eventoTrovato.azione_umana = bool(trovato.get("azione_umana"))
        eventoTrovato.visto = bool(trovato.get("visto"))
        return eventoTrovato
    
    def creaEvento(evento : Evento):
        """
            Questo metodo instanzia un evento sul database
        """
        eventi.insert_one({
            "titolo" : evento.titolo,
            "descrizione" : evento.descrizione,
            "orario" : evento.orario,
            "tipo" : evento.tipo,
            "azione_umana" : evento.azione_umana,
            "visto" : evento.visto
        })



