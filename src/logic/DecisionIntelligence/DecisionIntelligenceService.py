from src.logic.DecisionIntelligence.IAdapter import IAdapter


class DecisionIntelligenceService:  
    def getPredizioneLivelliIrrigazione(lon : float, lat : float, crop : str, stage : str):
        return IAdapter.getAiPrediction(lat, lon, crop, stage)