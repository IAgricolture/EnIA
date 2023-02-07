from src.logic.Adapters.NominatimAdapter import NominatimAdapter
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.Adapters.SenseSquareAdapter import SenseSquareAdapter
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.model.Evento import Evento
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.model.Terreno import Terreno
from src.logic.Storage.TerrenoDAO import TerrenoDAO
import requests
import json
import re
from datetime import datetime

#TODO: ERROR HANDLING DAO TERRENO
class AmbienteAgricoloService():
    
    ColturaEng = ["Barley", "Bean", "Cabbage", "Carrot", "Cotton", "Cucumber", "Eggplant", "Grain", "Lentil", "Lettuce"]
    Colture= ["Orzo", "Fagiolo", "Cavolo", "Carota", "Cotone", "Cetriolo", "Melanzana", "Grano", "Lenticchia", "Lattuga"]
    StadiCrescita = ["Iniziale", "Sviluppo", "Metà Stagione", "Fine Stagione"]
    
    def isValidTerreno(terreno: Terreno)->bool:
        risultato = AmbienteAgricoloService.validateTerreno(terreno)
        return risultato["esitoControllo"]
    
    def validateTerreno(terreno: Terreno):
        risultato = {
            "nomeNonValido": False,
            "colturaNonValida": False,
            "posizioneNonValida": False,
            "preferitoNonValido": False,
            "prioritaNonValida": False,
            "proprietarioNonValido": False,
            "stadio_crescitaNonValido": False,
            "esitoControllo": False 
        }
        regexNome = re.compile(r"[a-zA-z0-9_]+[\w\s\W]*$")
        regexPriorita = re.compile(r"^[0-9]")
        if(not re.match(regexNome, terreno.nome)):
            risultato["nomeNonValido"] = True
        if(terreno.coltura not in AmbienteAgricoloService.Colture):
            risultato["colturaNonValida"] = True
        posizione = terreno.posizione
        try: #Se non esiste uno dei campi richiesti, la posizione è invalida.
            if(posizione["type"] != "Feature"):  #Una sola posizione
                risultato["posizioneNonValida"] = True
            if(posizione["properties"]):    #Non ha proprietà aggiuntive
                risultato["posizioneNonValida"] = True 
            geometria = posizione["geometry"]
            if(geometria["type"] != "Polygon"):
                risultato["posizioneNonValida"] = True
            if(len(geometria["coordinates"][0]) < 2 or len(geometria["coordinates"][0][0]) != 2): #Ha un array di coordinate
                risultato["posizioneNonValida"] = True 
        except KeyError:
            risultato["posizioneNonValida"] = True
        if(terreno.preferito != True and terreno.preferito != False):
            risultato["preferitoNonValido"] = True   
        if(not re.match(regexPriorita, str(terreno.priorita))):
            risultato["prioritaNonValida"] = True
        if(terreno.stadio_crescita not in AmbienteAgricoloService.StadiCrescita):
            risultato["stadio_crescitaNonValido"] = True
        if not (risultato["nomeNonValido"] or risultato["colturaNonValida"] or risultato["posizioneNonValida"] or risultato["preferitoNonValido"] or risultato["prioritaNonValida"] or risultato["proprietarioNonValido"] or risultato["stadio_crescitaNonValido"]):
            risultato["esitoControllo"] = True
        return risultato
    
    def visualizzaTerreni(farmer:str):
        Terreni = TerrenoDAO.restituisciTerreniByFarmer(farmer)
        return Terreni
    
    def aggiungiTerreno(nome: str, coltura:str, stadio_crescita: str, posizione, preferito:bool, priorita:int, proprietario: str)-> bool:
        id = None
        terreno = Terreno(id, nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        risultato = AmbienteAgricoloService.validateTerreno(terreno)
        if(risultato["esitoControllo"]):
            resultDB = TerrenoDAO.InserisciTerreno(terreno)
            risultato["esitoOperazione"] = True
            risultato["restituito"] = resultDB
        else:
            risultato["esitoOperazione"] = False
            risultato["restituito"] = None
        return risultato

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
    
    def cercaPosizione(id:str) -> dict:
        terreno = TerrenoDAO.TrovaTerreno(id)
        if(terreno is None):
            return None
        else:
            #Estraggo latitudine e longitudine del primo punto del terreno, di cui prendo la posizione
            lat = terreno.posizione["geometry"]["coordinates"][0][0][1]
            lon = terreno.posizione["geometry"]["coordinates"][0][0][0]
            print(lat)
            print(lon)
            nominatim = NominatimAdapter(lat, lon, "json", 10)
            datiapi = nominatim.get_data()
            return datiapi  #JSON
        
    def cercaInquinamento(provincia:str, regione:str, nazione:str, comune:str):
        adapter = SenseSquareAdapter(nazione, regione, provincia, comune)
        datiapi = adapter.get_data_for_today()
        return datiapi
    
    def cercaStoricoInquinamento(dataInizio:str, dataFine:str, comune:str, regione:str, nazione:str, provincia:str, formato:str):
        adapter = SenseSquareAdapter(nazione, regione, provincia, comune, start_date = dataInizio, end_date = dataFine, formato = formato)
        datiapi = adapter.get_data_time_interval()
        return datiapi

    def aggiungiIrrigatore(id_terreno: str, nome_irrigatore: str, posizione_irrigatore: str) -> str:
        impianto = ImpiantoDiIrrigazione("", nome_irrigatore, "irrigatore", "", posizione_irrigatore, False)
        id = ImpiantoDiIrrigazioneDAO.creaImpianto(impianto, id_terreno)
        evento = Evento("", "Creazione Irrigatore", "L'irrigatore :" + nome_irrigatore + " è stato creato",datetime.now().isoformat(' ', 'seconds'), "INFO",False ,False, id_terreno)
        GestioneEventiService.creaEvento(evento)
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
        
    
    
    def restituisciPredizioneLivelliIrrigazione(lon:float, lat:float, crop:str, stage:str):
        return DecisionIntelligenceService.getPredizioneLivelliIrrigazione(lon, lat, crop, stage)
