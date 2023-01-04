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
        '''
        Questo metodo dato un id in input retituisce un terreno con l'id corrispondenti
        '''
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        if(trovato == None):
            return None
        id = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        coltura = str(trovato.get("coltura"))
        posizione = str(trovato.get("posizione"))
        preferito = bool(trovato.get("preferito"))
        priorita = int(str(trovato.get("priorita")))
        listautenti = str(trovato.get("listautenti"))
        temp = Terreno(id, nome, coltura, posizione, preferito, priorita, listautenti)
        return temp

    def RimuoviTerreno(terreno: Terreno):
        trovato = terreni.delete_one({"_id": ObjectId(id)})
        if trovato.deleted_count == 1:
            print("Eliminato")
        else:
            print("Errore nel eliminazione")
    
    def modificaTerreno(terreno : Terreno): 
        """ Il metodo modifica un'entità terreno presente nel database, trasformandola in quella passata come parametro."""  
        trovato = TerrenoDAO.TrovaTerreno(str(terreno.id))
        print(trovato.nome)
        if(trovato == None):
            return None
        terreni.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "nome" : terreno.nome,
            "coltura": terreno.coltura,
            "posizione": terreno.posizione,
            "preferito": terreno.preferito,
            "priorita": terreno.priorita,
            "listautenti" : terreno.listautenti,
        }})
