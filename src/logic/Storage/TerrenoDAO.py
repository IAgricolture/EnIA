from src.dbConnection import terreni
from src.logic.model.Terreno import Terreno
from flask import jsonify
import datetime
from bson.objectid import ObjectId

class TerrenoDAO():

    def InserisciTerreno(terreno : Terreno):
        """
        Questo metodo istanzia un oggetto AmbienteAgricolo sul database
        """
        terreni.insert_one({
            "Nome" : terreno.nome,
            "Coltura" : terreno.coltura,
            "Posizione" : terreno.posizione,
            "Preferito" : terreno.preferito,
            "Priorita" : terreno.priorita,
            "proprietario" : terreno.proprietario
        })


    def TrovaTerreno(id : str) -> Terreno:
        """
        Questo metodo dato un id in input retituisce un terrreno con l'id corrispondenti  
        """
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        if(trovato == None):
            return None
        id2 = str(trovato.get("_id"))
        nome = str(trovato.get("Nome"))
        coltura = str(trovato.get("Coltura"))
        posizione = trovato.get("Posizione")
        print(posizione)
        preferito = (trovato.get("Preferito"))
        priorita = int(trovato.get("Priorita"))  
        proprietario = str(trovato.get("proprietario"))
        NewTerreno = Terreno(id2,nome,coltura,posizione,preferito,priorita, proprietario)
        return NewTerreno


    def RimuoviTerreno(terreno : Terreno):
        trovato = terreni.delete_one({"_id" : ObjectId(terreno.id)})
        if trovato.deleted_count == 1:
            print("Eliminato")
        else:
            print("Errore nel eliminazione")

    def modificaTerreno(terrenoMod : Terreno): 
        """ Il metodo modifica un'entità terreno presente nel database, trasformandola in quella passata come parametro."""  
        trovato = TerrenoDAO.TrovaTerreno(str(terrenoMod.id))
        print(terrenoMod.preferito)
        if(trovato == None):
            return None
        return terreni.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "Nome" : terrenoMod.nome,
            "Coltura": terrenoMod.coltura,
            "Posizione": terrenoMod.posizione,
            "Preferito": terrenoMod.preferito,
            "Priorita": terrenoMod.priorita,
            "proprietario" : terrenoMod.proprietario,
        }})
    
    def restituisciTerreniByFarmer(farmer: str) -> list:
        """
        Questo metodo dato un id in input retituisce un terrreno con l'id corrispondenti  
        """
        trovati = terreni.find({"proprietario" : farmer})
        listaTerreni = []
        for trovato in trovati:
            id2 = str(trovato.get("_id"))
            nome = str(trovato.get("Nome"))
            coltura = str(trovato.get("Coltura"))
            posizione = trovato.get("Posizione")
            preferito = (trovato.get("Preferito"))
            priorita = int(trovato.get("Priorita"))  
            proprietario = str(trovato.get("proprietario"))
            NewTerreno = Terreno(id2,nome,coltura,posizione,preferito,priorita, proprietario)
            listaTerreni.append(NewTerreno)
        
        return listaTerreni