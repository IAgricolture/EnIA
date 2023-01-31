from src.logic.Adapters.IAdapter import IAdapter


class DecisionIntelligenceService():  
    '''
    Classe Service di Decision Inteligence

    ...

    Attributi
    ----------
    None

    Metodi
    getPredizioneLivelliIrrigazione(lon : float, lat : float, crop : str, stage : str)
        Dati i valori di latitudine, longitudine la tipologia di crops ed lo stato di crescita
        restiuisce le previsioni meteo 

    '''
    def getPredizioneLivelliIrrigazione(lon : float, lat : float, crop : str, stage : str):
        '''
        Dati i valori di latitudine, longitudine la tipologia di crops ed lo stato di crescita
        restiuisce le previsioni meteo 
        '''
        adapter = IAdapter(lat, lon, crop, stage)
        return adapter.getAiPrediction()