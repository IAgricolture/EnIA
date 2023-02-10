import datetime
import requests


class IAdapter:
    irrigazione_translator = {
        0: "Nessuno",
        1: "Basso",
        2: "Medio",
        3: "Elevato"}
    crop_translator = {
        "Orzo": "Barley",
        "Fagiolo": "Bean",
        "Cavolo": "Cabbage",
        "Carota": "Carrot",
        "Cotone": "Cotton",
        "Cetriolo": "Cucumber",
        "Melanzana": "Eggplant",
        "Grano": "Grain",
        "Lenticchia": "Lentil",
        "Lattuga": "Lettuce"}
    growth_translator = {
        "Iniziale": "InitialStage",
        "Sviluppo": "CropDevStage",
        "Metà Stagione": "MidSeasonStage",
        "Fine Stagione": "LateSeasonStage"}

    def __init__(self, lat, lon, crop, stage):
        # traduci crop e stage
        crop = IAdapter.crop_translator.get(crop)
        stage = IAdapter.growth_translator.get(stage)
        
        if crop == None:
            raise Exception("Coltura non valida")
        
        if stage == None:
            raise Exception("Stadio di crescita non valido")
        
        #se non si possono tradurre lancia eccezione
        if crop == None or stage == None or lat == None or lon == None:
            raise Exception("None value not allowed")
        
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            raise Exception("Latitudine o longitudine non valide")
        
        
        self.lat = lat
        self.lon = lon
        self.crop = crop
        self.stage = stage

    def getAiPrediction(self):
        fetch = requests.get("https://benedettoscala.pythonanywhere.com/getIrrigationDecision?"
                             "lat=" + str(self.lat) + "&lon=" + str(self.lon) +
                             "&crop=" + str(self.crop) + "&growthStage=" + str(self.stage))

        # get json body
        predizioni = fetch.json()["irrigationLevel"]

        # impacchetta per data
        livello_irrigazione = {}
        giorno = datetime.datetime.now()

        for p in predizioni:
            # formatta giorno a dd-mm-yyyy
            giorno_formattato = giorno.strftime("%d-%m-%Y")
            livello_irrigazione[giorno_formattato] = IAdapter.irrigazione_translator[p]
            giorno = giorno + datetime.timedelta(days=1)
        print(livello_irrigazione)
        return livello_irrigazione   