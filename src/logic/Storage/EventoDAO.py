import datetime
from src.dbConnection import eventi
from src.logic.model.Evento import Evento
from flask import jsonify
from bson.objectid import ObjectId


class EventoDAO():
    
    '''
    Classe DAO di Evento

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    findEvento(id: str):
        Questo metodo trova un Evento sul database, usando il suo ObjectId
    creaEvento(evento: Evento):
        Questo metodo ci permette l'istanziazione di un evento sul database
    findEventiByTerreno(idTerreno: str):       
        Questo metodo trova gli eventi associati ad un detereminato terreno grazie da suo id passato in input 
    cancellaTuttiEventiByTerreno(idTerreno: str):
        Questo metodo cancella gli eventi associati ad un detereminato terreno grazie da suo id passato in input
    cancellaEvento(idEvento: str):
        Questo metodo cancella un evento specifico trimite il suo id
    

    '''

    def findEvento(id: str) -> Evento:
        
        '''
        Questo metodo trova un Evento sul database, usando il suo ObjectId

        Parametri
        ----------
        id : str
            id dell Evento

        Returns
        -------
        eventoTrovato : Evento
            Restituisce l'evento avente come id quello passato in input
        '''
        
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
        
        '''
        Questo metodo ci permette l'istanziazione di un evento sul database

        Parametri
        ----------
        evento : Evento
            evento da creare

        Returns
        -------
        result.inserted_id : str
            id dell evento appena creato
        '''
        
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
        '''
        Questo metodo trova gli eventi associati ad un detereminato terreno grazie da suo id passato in input

        Parametri
        ----------
        idTerreno : str
            id del Terreno

        Returns
        -------
        eventiTrovati : list Eventi
            Restituisce la lista degli eventi
        '''
        
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
        '''
        Questo metodo cancella gli eventi associati ad un detereminato terreno grazie da suo id passato in input

        Parametri
        ----------
        idTerreno : str
            id del Terreno

        Returns
        -------
        '''
        
        eventi.delete_many({"terreno": idTerreno})

    def cancellaEvento(idEvento: str):
        '''
        Questo metodo cancella un evento specifico trimite il suo id

        Parametri
        ----------
        idEvento : str
            id dell evento

        Returns
        -------
        '''
        
        eventi.delete_one({"_id": ObjectId(idEvento)})
