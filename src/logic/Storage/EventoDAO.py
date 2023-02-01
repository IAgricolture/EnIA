import datetime
from src.dbConnection import eventi
from src.logic.model.Evento import Evento
from flask import jsonify
from bson.objectid import ObjectId


class EventoDAO():

    def findEvento(id: str) -> Evento:
        """
            Questo metodo trova un Evento sul database, usando il suo ObjectId
            :return: Evento
        """
        trovato = eventi.find_one({"_id": ObjectId(id)})
        id = str(trovato.get("_id"))
        titolo = str(trovato.get("titolo"))
        descrizione = str(trovato.get("descrizione"))
        orario = trovato.get("orario")
        tipo = str(trovato.get("tipo"))
        azione_umana = bool(trovato.get("azione_umana"))
        visto = bool(trovato.get("visto"))
        eventoTrovato = Evento(
            id,
            titolo,
            descrizione,
            orario,
            tipo,
            azione_umana,
            visto)
        return eventoTrovato

    def creaEvento(evento: Evento) -> str:
        """
            Questo metodo instanzia un evento sul database
        """
        result = eventi.insert_one({
            "titolo": evento.titolo,
            "descrizione": evento.descrizione,
            "orario": evento.orario,
            "tipo": evento.tipo,
            "azione_umana": evento.azione_umana,
            "visto": evento.visto,
            "terreno": evento.terreno
        })

        return str(result.inserted_id)

    def findEventiByTerreno(idTerreno: str):
        # trova eventi sul database con l'id del terreno
        print(idTerreno)
        eventiTrovati = eventi.find({"terreno": idTerreno})
        eventiTrovati = list(eventiTrovati)

        # cast all datetime object to string
        for evento in eventiTrovati:
            evento["_id"] = str(evento["_id"])
            evento["orario"] = str(evento["orario"])
        print(list(eventiTrovati))

        return list(eventiTrovati)

    def cancellaTuttiEventiByTerreno(idTerreno: str):
        eventiTrovati = eventi.delete_many({"terreno": idTerreno})

    def cancellaEvento(idEvento: str):
        eventiTrovati = eventi.delete_one({"_id": ObjectId(idEvento)})
