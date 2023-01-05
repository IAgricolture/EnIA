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


    def TrovaID(id : str) -> Terreno:
        """
        Questo metodo dato un id in input retituisce un terrreno con l'id corrispondenti  
        """
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        id2 = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        coltura = str(trovato.get("coltura"))
        posizione = str(trovato.get("posizione"))
        preferito = bool(trovato.get("preferito"))
        priorita = trovato.get("priorita")   
        listautenti = str(trovato.get("listautenti"))
        NewTerreno = Terreno(id2,nome,coltura,posizione,preferito,priorita,listautenti)
        return NewTerreno
    

    def RimuoviTerreno(terreno : Terreno):
        trovato = terreni.delete_one({"_id" : ObjectId(id)})
        if trovato.deleted_count == 1:
            print("Eliminato")
        else:
            print("Errore nel eliminazione")

