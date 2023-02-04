from src.dbConnection import impianti
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from flask import jsonify
from bson.objectid import ObjectId


class ImpiantoDiIrrigazioneDAO():


    def findImpiantiByTerreno(idTerreno:str):
        #trova impianti sul database con l'id del terreno
        impiantiTrovati = impianti.find({"terreno" : ObjectId(idTerreno)})
        impiantiTrovati = list(impiantiTrovati)
        
        #cast all objectid to string
        for impianto in impiantiTrovati:
            impianto["_id"] = str(impianto["_id"])
            impianto["terreno"] = str(impianto["terreno"])
        
        
        return list(impiantiTrovati)

    def findImpiantoById(id : str) -> ImpiantoDiIrrigazione:
        """
            Questo metodo trova un Impianto di irrigazione sul database, usando il suo ObjectId
            :return: ImpiantoDiIrrigazione
        """
        trovato = impianti.find_one({"_id" : ObjectId(id)})
        
        id = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        tipo = str(trovato.get("tipo"))
        codice = str(trovato.get("codice"))
        attivo = bool(trovato.get("attivo"))
        posizione = trovato.get("posizione")

        impiantoTrovato = ImpiantoDiIrrigazione(id, nome, tipo, codice, posizione, attivo)

        return impiantoTrovato
    
    def creaImpianto(impianto : ImpiantoDiIrrigazione, idTerreno: str) -> str:
        """
            Questo metodo instanzia un impianto di irrigazione sul database
        """  
           
        result = impianti.insert_one({
            "nome" : impianto.nome,
            "tipo" : impianto.tipo,
            "codice" : impianto.codice,
            "attivo" : impianto.attivo,
            "posizione": impianto.posizione,
            "terreno": ObjectId(idTerreno)
        })
        
        return str(result.inserted_id)
    
    def modificaImpianto(impianto : ImpiantoDiIrrigazione):
        """
            Questo metodo modifica un impianto di irrigazione sul database
        """  
        impianti.update_one(
            {"_id" : ObjectId(impianto.id)},
            {
                "$set" : {
                    "nome" : impianto.nome,
                    "tipo" : impianto.tipo,
                    "codice" : impianto.codice,
                    "attivo" : impianto.attivo,
                    "posizione": impianto.posizione
                }
            }
        )
    
    def attivaImpianto(id : str):
        """
            Questo metodo attiva un impianto di irrigazione sul database
        """  
        result = impianti.update_one(
            {"_id" : ObjectId(id)},
            {
                "$set" : {
                    "attivo" : True
                }
            }
        )
        #se non è stato trovato nessun impianto con quell'id
        return result.modified_count == 1
    
    def disattivaImpianto(id : str):
        """
            Questo metodo disattiva un impianto di irrigazione sul database
        """  
        result = impianti.update_one(
            {"_id" : ObjectId(id)},
            {
                "$set" : {
                    "attivo" : False
                }
            }
        )
        #se non è stato trovato nessun impianto con quell'id
        return result.modified_count == 1
    
    def eliminaImpianto(id : str):
        """
            Questo metodo elimina un impianto di irrigazione sul database
        """  
        result = impianti.delete_one({"_id" : ObjectId(id)})
        if(result.deleted_count == 1):
            return True
        else:
            return False
        





