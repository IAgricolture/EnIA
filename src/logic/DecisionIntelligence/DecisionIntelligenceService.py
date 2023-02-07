from src.logic.Adapters.IAdapter import IAdapter
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.model.Evento import Evento

class DecisionIntelligenceService:  
    def getPredizioneLivelliIrrigazione(lon : float, lat : float, crop : str, stage : str):
        try:
            adapter = IAdapter(lat, lon, crop, stage)
            return adapter.getAiPrediction()
        except Exception as e:
            raise e
        
    def cercaMeteo(lat:float, lon:float):
        #creo l'oggetto meteo
        meteo = OpenMeteoAdapter(lat, lon)
        data = meteo.get_data()
        
        #fai la somma delle precipitazioni per le prossime 24 ore
        somma = 0
        for i in range(0,24):
            somma += data["hourly"]["precipitation"][i]
        
        if somma > 10:
            u = Evento("", "Pioggia", "Ci saranno ingenti quantità di pioggia nelle prossime 24 ore", datetime.now().isoformat(' ', 'seconds'), "Pioggia", False, False, "")
            GestioneEventiService.creaEvento(u)
        
        return data