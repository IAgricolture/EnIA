from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.Storage.ScheduleDAO import ScheduleDAO


class GestioneScheduleService:
    
    def trovaScheduleTerreno(idTerreno : str):
        schedule_settimanale = ScheduleDAO.getWeeklySchedule(idTerreno)
        dict = {}
        #push in dict the schedule
        for i in range(0, 7):
            dict[schedule_settimanale[i].get("inizio")] = schedule_settimanale[i].get("modalita")
        return dict
    
    def modificaLivelloSchedule(id_terreno: str, data: str, modalita: str):
        ScheduleDAO.modificaLivelloSchedule(id_terreno, data, modalita)
        return True
    
    def usaSchedulingConsigliato(id_terreno: str, lat: float, lon: float, stage: str, coltura: str):
        dict = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, coltura, stage)
        #per ogni data nel dizionario
        for data in dict:
            #modifica il livello di irrigazione
            ScheduleDAO.modificaLivelloSchedule(id_terreno, data, dict.get(data))
        return True