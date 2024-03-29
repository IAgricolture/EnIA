import datetime
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.Storage.ScheduleDAO import ScheduleDAO
from src.logic.model.Evento import Evento


class GestioneScheduleService:
    
    def trovaScheduleTerreno(idTerreno : str):
        schedule_settimanale = ScheduleDAO.getWeeklySchedule(idTerreno)
        dict = {}
        #push in dict the schedule
        for i in range(0, 7):
            dict[schedule_settimanale[i].get("inizio")] = schedule_settimanale[i].get("modalita")
        return dict
    
    def modificaLivelloSchedule(id_terreno: str, data: str, modalita: str):
        result = ScheduleDAO.modificaLivelloSchedule(id_terreno, data, modalita)
        return result
    
    def usaSchedulingConsigliato(id_terreno: str, lat: float, lon: float, stage: str, coltura: str):
        dict = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, coltura, stage)
        result = True
        #per ogni data nel dizionario
        for data in dict:
            #modifica il livello di irrigazione
            result = ScheduleDAO.modificaLivelloSchedule(id_terreno, data, dict.get(data))
            #se result è false, esce dal ciclo
            if result == False:
                print("errore nell'aggiornamento dello schedule")
                break
            
        evento = Evento("", "Scheduling", "Scheduling consigliato applicato", datetime.datetime.now().isoformat(' ', 'seconds'), "Scheduling", False, False, id_terreno)
        GestioneEventiService.creaEvento(evento)
        return result