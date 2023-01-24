

import datetime
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.model.Evento import Evento

class GestioneEventiService():
    
    def creaEvento(evento : Evento):
        EventoDAO.creaEvento(evento)
    
    def visualizzaEventiByTerreno(idTerreno:str):
        eventiTrovati = EventoDAO.findEventiByTerreno(idTerreno)
        return eventiTrovati
        


