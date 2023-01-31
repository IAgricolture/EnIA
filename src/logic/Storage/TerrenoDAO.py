from src.dbConnection import terreni
from src.logic.model.Terreno import Terreno
from flask import jsonify
import datetime
from bson.objectid import ObjectId

class TerrenoDAO():

    def InserisciTerreno(terreno : Terreno) -> str:
        """
        Questo metodo istanzia un oggetto AmbienteAgricolo sul database
        """
        result = terreni.insert_one({
            "Nome" : terreno.nome,
            "Coltura" : terreno.coltura,
            "Posizione" : terreno.posizione,
            "Preferito" : terreno.preferito,
            "Priorita" : terreno.priorita,
            "proprietario" : terreno.proprietario,
            "stadio_crescita" : terreno.stadio_crescita
        })
        
        return str(result.inserted_id)


    def TrovaTerreno(id : str) -> Terreno:
        """
        Questo metodo dato un id in input retituisce un terrreno con l'id corrispondenti  
        """
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        if(trovato is None):
            return None
        id2 = str(trovato.get("_id"))
        nome = str(trovato.get("Nome"))
        coltura = str(trovato.get("Coltura"))
        posizione = trovato.get("Posizione")
        preferito = (trovato.get("Preferito"))
        priorita = int(trovato.get("Priorita"))  
        proprietario = str(trovato.get("proprietario"))
        stadio_crescita = str(trovato.get("stadio_crescita"))
        NewTerreno = Terreno(id2,nome,coltura, stadio_crescita,posizione,preferito,priorita, proprietario)
        return NewTerreno


    def RimuoviTerreno(terreno : Terreno)->bool:
        trovato = terreni.delete_one({"_id" : ObjectId(terreno.id)})
        if trovato.deleted_count == 1:
            return True
        else:
            return False

    def modificaTerreno(terrenoMod : Terreno): 
        """ Il metodo modifica un'entità terreno presente nel database, trasformandola in quella passata come parametro."""  
        trovato = TerrenoDAO.TrovaTerreno(str(terrenoMod.id))
        if(trovato is None):
            return None
        return terreni.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "Nome" : terrenoMod.nome,
            "Coltura": terrenoMod.coltura,
            "Posizione": terrenoMod.posizione,
            "Preferito": terrenoMod.preferito,
            "Priorita": terrenoMod.priorita,
            "proprietario" : terrenoMod.proprietario,
            "stadio_crescita" : terrenoMod.stadio_crescita
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
            stadio_crescita = str(trovato.get("stadio_crescita"))
            NewTerreno = Terreno(id2,nome,coltura,stadio_crescita,posizione,preferito,priorita, proprietario)
            listaTerreni.append(NewTerreno)
        
        return listaTerreni
