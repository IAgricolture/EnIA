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
            "ListaUtenti" : terreno.listautenti 
        })


    def TrovaTerreno(id : str) -> Terreno:
        """
        Questo metodo dato un id in input retituisce un terrreno con l'id corrispondenti  
        """
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        if(trovato == None):
            return None
        id2 = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        coltura = str(trovato.get("coltura"))
        posizione = str(trovato.get("posizione"))
        preferito = bool(trovato.get("preferito"))
        priorita = trovato.get("priorita")   
        NewTerreno = Terreno(id2,nome,coltura,posizione,preferito,priorita)
        return NewTerreno


    def RimuoviTerreno(terreno : Terreno):
        trovato = terreni.delete_one({"_id" : ObjectId(id)})
        if trovato.deleted_count == 1:
            print("Eliminato")
        else:
            print("Errore nel eliminazione")

    def modificaTerreno(terrenoMod : Terreno): 
        """ Il metodo modifica un'entità terreno presente nel database, trasformandola in quella passata come parametro."""  
        trovato = TerrenoDAO.TrovaTerreno(str(terrenoMod.id))
        print(trovato.nome)
        if(trovato == None):
            return None
        terreni.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "nome" : terrenoMod.nome,
            "coltura": terrenoMod.coltura,
            "posizione": terrenoMod.posizione,
            "preferito": terrenoMod.preferito,
            "priorita": terrenoMod.priorita,
            "listautenti" : terrenoMod.listautenti,
        }})