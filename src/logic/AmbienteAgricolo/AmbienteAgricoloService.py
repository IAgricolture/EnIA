from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.model.Terreno import Terreno
from src.logic.Storage.TerrenoDAO import TerrenoDAO
import requests
import json
from datetime import datetime

#TODO: ERROR HANDLING DAO TERRENO
class AmbienteAgricoloService():
    
    ColturaEng = ["Barley", "Bean", "Cabbage", "Carrot", "Cotton", "Cucumber", "Eggplant", "Grain", "Lentil", "Lettuce"]
    Colture= ["Orzo", "Fagiolo", "Cavolo", "Carota", "Cotone", "Cetriolo", "Melanzana", "Grano", "Lenticchia", "Lattuga"]
    StadiCrescita = ["Iniziale", "Sviluppo", "Metà Stagione", "Fine Stagione"]
    
    def visualizzaTerreni(farmer:str):
        Terreni = TerrenoDAO.restituisciTerreniByFarmer(farmer)
        return Terreni
    
    def aggiungiTerreno(nome: str, coltura:str, stadio_crescita: str, posizione, preferito:bool, priorita:int, proprietario: str)-> bool:
        id = None
        terreno = Terreno(id, nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        result = TerrenoDAO.InserisciTerreno(terreno)
        return result != None

    def trovaTerreno(id: str)-> Terreno:
        Terreno = TerrenoDAO.TrovaTerreno(id)
        return Terreno
    
    def modificaTerreno(id:str, nome: str, coltura:str, stadio_crescita: str, posizione, preferito:bool, priorita:int, proprietario: str)-> bool:
        terreno = Terreno(id, nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        result = TerrenoDAO.modificaTerreno(terreno)
        return result.matched_count > 0 #Restituisce True se andato bene, False altrimenti.
    
    def eliminaTerreno(id:str)-> bool:
        terreno = TerrenoDAO.TrovaTerreno(id)
        if(terreno is None):
            return False
        else:
            TerrenoDAO.RimuoviTerreno(terreno)
            return True
    
    def cercaPosizione(id:str):
        terreno = TerrenoDAO.TrovaTerreno(id)
        if(terreno is None):
            return None
        else:
            #Estraggo latitudine e longitudine del primo punto del terreno, di cui prendo la posizione
            lat = terreno.posizione["geometry"]["coordinates"][0][0][1]
            lon = terreno.posizione["geometry"]["coordinates"][0][0][0]
            print(lat)
            print(lon)
            datiapi = requests.get("https://nominatim.openstreetmap.org/reverse?lat="+ str(lat) + "&lon=" + str(lon) + "&format=json&zoom=10").json()
            print(datiapi)
            return datiapi  #JSON
        
    def cercaInquinamento(provincia:str, regione:str, nazione:str, comune:str):
        currentdate = str(datetime.now()).split(" ")
        date = currentdate[0]
        precisehour = currentdate[1].split(":")
        time = precisehour[0] + ":" + precisehour[1]
        url = "https://square.sensesquare.eu:5001/placeView"
        body = {
            "apikey": "3BK3D0LWE8DQ", #Codice API, NON MODIFICARE
            "tempo": "giorno",
            "date": date,
            "time": time,
            "nazione": nazione,
            "regione": regione,
            "provincia": provincia,
            "comune": comune,
            "zoom": "3", #0 per tutte le nazioni, 1 per tutte le regioni, 2 per tutte le province, 3 per tutti i comuni, 4 NON VA
            "predictions": "true", #NON TOCCARE
            "fonti":"[]" #NON TOCCARE
            }
        datiapi = requests.post(url=url, data = body).json()
        print(datiapi)
        return datiapi
    
    def cercaStoricoInquinamento(dataInizio:str, dataFine:str, comune:str, regione:str, nazione:str, provincia:str, formato:str):
        url = "https://square.sensesquare.eu:5001/download"
        body = {
            "apikey": "3BK3D0LWE8DQ",
            "req_type": "daily",
            "zoom": "3",
            "start_date": dataInizio,    #Formato deve essere YYYY-MM-DD
            "start_hour": "0",
            "end_date": dataFine,
            "end_hour": "0",
            "nazione": nazione,
            "regione": regione,
            "provincia": provincia,
            "comune": comune,
            "format": formato
        }
        datiapi = requests.post(url=url, data = body).text
        print(datiapi)
        if(formato == "json"):  ##Multipli oggetti JSON, ne faccio un parse decente in un array di oggetti json.
            arrayDati = datiapi.split("\n") #Ne ottengo un array
            print(arrayDati)
            print(len(arrayDati))
            arrayDati.pop(len(arrayDati) - 1) #Rimuovo un elemento vuoto creato con lo split, all'ultimo posto
            return arrayDati
        else:
            return datiapi  #Qualsiasi altro formato, è buono così com'è.

    def aggiungiIrrigatore(id_terreno: str, nome_irrigatore: str, posizione_irrigatore: str) -> str:
        impianto = ImpiantoDiIrrigazione("", nome_irrigatore, "irrigatore", "", posizione_irrigatore, False)
        id = ImpiantoDiIrrigazioneDAO.creaImpianto(impianto, id_terreno)
        return id
    
    def modificaIrrigatore(idIrrigatore: str, nomeIrrigatore: str, posizioneIrrigatore: str):
        impianto = ImpiantoDiIrrigazione(idIrrigatore, nomeIrrigatore, "irrigatore", "", posizioneIrrigatore, False)
        ImpiantoDiIrrigazioneDAO.modificaImpianto(impianto)
        return True
    
    def getIrrigatore(idIrrigatore: str):
        return ImpiantoDiIrrigazioneDAO.findImpiantoById(idIrrigatore)
    
    def visualizzaListaIrrigatori(idTerreno: str):
        return ImpiantoDiIrrigazioneDAO.findImpiantiByTerreno(idTerreno)
    
    def eliminaIrrigatore(idIrrigatore: str):
        return ImpiantoDiIrrigazioneDAO.eliminaImpianto(idIrrigatore)
    
    def attivaDisattivaIrrigatore(idIrrigatore:str):
        if(ImpiantoDiIrrigazioneDAO.findImpiantoById(idIrrigatore).attivo == True):
            ImpiantoDiIrrigazioneDAO.disattivaImpianto(idIrrigatore)
            return False
        else:
            ImpiantoDiIrrigazioneDAO.attivaImpianto(idIrrigatore)
            return True
        
    def visualizzaListaEventi(idTerreno: str):
        return EventoDAO.findEventiByTerreno(idTerreno)
    
    
    def cercalat(id:str):
        terreno = TerrenoDAO.TrovaTerreno(id)
        if(terreno is None):
            return None
        else:
            #Estraggo latitudine e longitudine del primo punto del terreno, di cui prendo la posizione
            lat = terreno.posizione["geometry"]["coordinates"][0][0][1]
            return lat
        
    def cercalon(id:str):
        terreno = TerrenoDAO.TrovaTerreno(id)
        if(terreno is None):
            return None
        else:
            #Estraggo latitudine e longitudine del primo punto del terreno, di cui prendo la posizione
            lon = terreno.posizione["geometry"]["coordinates"][0][0][0]
            return lon
        
    def cercaMeteo(lat:float, lon:float):
        url = "https://api.open-meteo.com/v1/forecast?"\
        "latitude="+str(lat)+"&longitude="+str(lon)+ "&hourly=temperature_2m,relativehumidity_2m,precipitation"
        data = requests.get(url).json()
        print(data)
        return data
    
    def restituisciPredizioneLivelliIrrigazione(lon:float, lat:float, crop:str, stage:str):
        return DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, crop, stage)
