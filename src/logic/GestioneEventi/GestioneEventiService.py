

import datetime
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.model.Evento import Evento

class GestioneEventiService():
    '''
    Classe Service di Eventi

    ...

    Attributi
    ----------
    None

    Metodi
    creaEvento(evento : Evento):
        Creazione di un nuovo evento
    visualizzaEventiByTerreno(idTerreno:str):
        Recupera nel DB gli eventi associati ad un terreno tramite id
    cancellaTuttiEventiByTerreno(idTerreno:str):
        Cancella tutti gli eventi associati ad un terreno
    cancellaEvento(idEvento:str):

    '''
    def creaEvento(evento : Evento):
        '''
        Creazione di un nuovo evento

        Parametri
        ----------
        Evento : evento
            L'evento da creare

        Returns
        -------
        '''
        EventoDAO.creaEvento(evento)
    
    def visualizzaEventiByTerreno(idTerreno:str):
        '''
        Recupera nel DB gli eventi associati ad un terreno tramite id

        Parametri
        ----------
        idTerreno : str
            Id del terreno

        Returns
        -------
        eventiTrovati
            Restituisce gli eventi trovati
        '''
        eventiTrovati = EventoDAO.findEventiByTerreno(idTerreno)
        return eventiTrovati
    
    def cancellaTuttiEventiByTerreno(idTerreno:str):
        '''
        Cancella nel DataBase tutti gli eventi associati ad un terreno tramite id

        Parametri
        ----------
        idTerreno : str
            Id del terreno

        Returns
        -------
        '''
        EventoDAO.cancellaTuttiEventiByTerreno(idTerreno)
        
    def cancellaEvento(idEvento:str):
        '''
        Cancella DataBase l'evento associato ad un terreno tramite id

        Parametri
        ----------
        idTerreno : str
            Id del terreno

        Returns
        -------
        '''
        EventoDAO.cancellaEvento(idEvento)

