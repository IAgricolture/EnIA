import datetime
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.Storage.ScheduleDAO import ScheduleDAO
from src.logic.model.Evento import Evento


class GestioneScheduleService:
    '''
    Classe Service di Autenticazione

    ...

    Attributi
    ----------
    None

    Metodi
    trovaScheduleTerreno(idTerreno : str):
        Recupera i dati riguardanti lo schedule per l'irrigazione per il terreno passato in input
    modificaLivelloSchedule(id_terreno: str, data: str, modalita: str):

    usaSchedulingConsigliato(id_terreno: str, lat: float, lon: float, stage: str, coltura: str):

    '''
    def trovaScheduleTerreno(idTerreno : str):
        '''
        Recupera i dati riguardanti lo schedule per l'irrigazione per il terreno passato in input

        Parametri
        ----------
        idTerreno : str
            id del Terreno

        Returns
        -------
        dict : dict
            Schedule salvato nel DataBase
        '''
        schedule_settimanale = ScheduleDAO.getWeeklySchedule(idTerreno)
        dict = {}
        #push in dict the schedule
        for i in range(0, 7):
            dict[schedule_settimanale[i].get("inizio")] = schedule_settimanale[i].get("modalita")
        return dict
    
    def modificaLivelloSchedule(id_terreno: str, data: str, modalita: str):
        '''
        Aggiorna le informazioni sul database in base alle informaizoni passate in input 

        Parametri
        ----------
        id_terreno: str 
            id del Terrreno
        data: str
            Variabile riferita alla data in vui esegluimo la modifica
        modalita: str
            Variabile che indica la modalita di irrigazione

        Returns
        -------
        True : bool
            Esito della modifica
        '''
        ScheduleDAO.modificaLivelloSchedule(id_terreno, data, modalita)
        return True
    
    def usaSchedulingConsigliato(id_terreno: str, lat: float, lon: float, stage: str, coltura: str):
        '''
        Setta lo Scheduling in base alle inforrmazione risultanti dalle previsioni su quel determinato terreno 

        Parametri
        ----------
        id_terreno: str
            id del Terreno
        lat: float
            Latitudine del Terreno
        lon: float
            Longitudine del Terreno
        stage: str
            Livello di crescita 
        coltura: str
            Tipologia di coltivazione in quel terreno

        Returns
        -------
        True : bool
            Esito positivo 
        '''
        dict = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, coltura, stage)
        #per ogni data nel dizionario
        for data in dict:
            #modifica il livello di irrigazione
            ScheduleDAO.modificaLivelloSchedule(id_terreno, data, dict.get(data))
            
        evento = Evento("", "Scheduling", "Scheduling consigliato applicato", datetime.datetime.now(), "Scheduling", False, False, id_terreno)
        GestioneEventiService.creaEvento(evento)
        return True