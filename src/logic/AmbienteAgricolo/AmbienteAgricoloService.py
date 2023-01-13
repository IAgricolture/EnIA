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
        
    def cercaInquinamento(comune:str, regione:str, nazione:str):
        url = "https://square.sensesquare.eu:5001/placeView"
        body = {
            "apikey": "3BK3D0LWE8DQ", #Codice API, NON MODIFICARE
            "tempo": "giorno",
            "date": "2022-11-28",
            "time": "00:00",
            "nazione": nazione,
            "regione": regione,
            "provincia": comune,
            "zoom": "3", #0 per tutte le nazioni, 1 per tutte le regioni, 2 per tutte le province, 3 per tutti i comuni
            "predictions": "true", #NON TOCCARE
            "fonti":"[]" #NON TOCCARE
            }
        datiapi = requests.post(url=url, data = body).json()
        print(datiapi)
        return datiapi