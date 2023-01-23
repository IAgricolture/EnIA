import datetime
import requests


class IAdapter:
    irrigazione_translator = {0:"Nessuno", 1: "Basso", 2: "Medio", 3: "Elevato"}
    crop_translator = {"Orzo": "Barley", "Fagiolo": "Bean", "Cavolo": "Cabbage", "Carota": "Carrot", "Cotone": "Cotton", "Cetriolo": "Cucumber", "Melanzana": "Eggplant", "Grano": "Grain", "Lenticchia": "Lentil", "Lattuga": "Lettuce"}
    growth_translator = {"Iniziale": "InitialStage", "Sviluppo": "CropDevStage", "Metà Stagione": "MidSeasonStage", "Fine Stagione": "LateSeasonStage"}
    def getAiPrediction(lat: float, lon: float, crop: str, stage: str):
        #traduci crop e stage
        crop = IAdapter.crop_translator.get(crop)
        stage = IAdapter.growth_translator.get(stage)
        
        #controllo traduzione
        if crop == None or stage == None:
            return None
        
        fetch = requests.get("https://benedettoscala.pythonanywhere.com/getIrrigationDecision?"
                             "lat="+ str(lat) + "&lon=" + str(lon) +
                             "&crop="+ str(crop) + "&growthStage=" + str(stage))
        
        #get json body
        predizioni = fetch.json()["irrigationLevel"]
        
        #impacchetta per data
        livello_irrigazione = {}
        giorno = datetime.datetime.now()
        
        for p in predizioni:
            #formatta giorno a dd-mm-yyyy
            giorno_formattato = giorno.strftime("%d-%m-%Y")
            livello_irrigazione[giorno_formattato] = IAdapter.irrigazione_translator[p]
            giorno = giorno + datetime.timedelta(days=1)
        
        return livello_irrigazione   
    