from src.logic.model.dbConnection import terreni
from src.logic.model.Terrenoentity import Terreno
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
        trovato = terreni.find_one({"_id" : ObjectId(id)})
        temp = Terreno()
        temp.id = str(trovato.get("_id"))
        temp.nome = str(trovato.get("nome"))
        temp.coltura = str(trovato.get("coltura"))
        temp.posizione = str(trovato.get("posizione"))
        temp.preferito = bool(trovato.get("preferito"))
        temp.priorita = int(str(trovato.get("priorita")))
        temp.listautenti = str(trovato.get("listautenti"))
        return temp
    
