from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.model.Terreno import Terreno
from src.logic.Storage.TerrenoDAO import TerrenoDAO
import requests

#TODO: ERROR HANDLING DAO TERRENO
class AmbienteAgricoloService():
    def aggiungiTerreno(nome: str, coltura:str, posizione, preferito:bool, priorita:int)-> bool:
        id = None
        terreno = Terreno(id, nome, coltura, posizione, preferito, priorita)
        TerrenoDAO.InserisciTerreno(terreno)
        return True 

    def trovaTerreno(id: str)-> Terreno:
        Terreno = TerrenoDAO.TrovaTerreno(id)
        return Terreno
    
    def modificaTerreno(id:str, nome: str, coltura:str, posizione, preferito:bool, priorita:int)-> bool:
        terreno = Terreno(id, nome, coltura, posizione, preferito, priorita)
        TerrenoDAO.modificaTerreno(terreno)
        return True
    
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
        
        