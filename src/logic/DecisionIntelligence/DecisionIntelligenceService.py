from src.logic.Adapters.IAdapter import IAdapter


class DecisionIntelligenceService:  
    def getPredizioneLivelliIrrigazione(lon : float, lat : float, crop : str, stage : str):
        adapter = IAdapter(lat, lon, crop, stage)
        return adapter.getAiPrediction()