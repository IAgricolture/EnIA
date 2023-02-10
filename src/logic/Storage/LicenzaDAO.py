
from src.dbConnection import licenze
from src.logic.model.Licenza import Licenza
from flask import jsonify
from bson.objectid import ObjectId


class LicenzaDAO():
    
    '''
    Classe DAO di Licenza

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    findLicenza(id: str):
        Questo metodo trova una licenza sul database, usando il suo ObjectId
    creaLicenza(licenza: Licenza):
        Questo metodo instanzia una licenza sul database
    findLicenzaByProprietario(id: str):        
        Questo metodo trova una licenza non scaduta sul database, usando l'identificativo del suo proprietario

    '''
    
    def findLicenza(id: str) -> Licenza:
        '''
        Questo metodo trova una licenza sul database, usando il suo ObjectId

        Parametri
        ----------
        id: str
            id del Utente

        Returns
        -------
        utenteTrovato : utente
            Restituisce l'utente desiderato
        '''
        trovato = licenze.find_one({"_id": ObjectId(id)})

        id = str(trovato.get("_id"))
        tipo = trovato.get("tipo")
        costo = trovato.get("costo")
        data_attivazione = trovato.get("data_attivazione")
        data_scadenza = trovato.get("data_scadenza")
        scaduta = trovato.get("scaduta")
        proprietario = trovato.get("proprietario")

        licenzaTrovata = Licenza(
            id,
            tipo,
            costo,
            data_attivazione,
            data_scadenza,
            scaduta,
            proprietario)

        return licenzaTrovata

    def creaLicenza(licenza: Licenza) -> str:
        '''
        Questo metodo instanzia una licenza sul database
        
        Parametri
        ----------
        id: str
            id del Utente

        Returns
        -------
        utenteTrovato : utente
            Restituisce l'utente desiderato
        '''
        
        result = licenze.insert_one({
            "tipo": licenza.tipo,
            "costo": licenza.costo,
            "data_attivazione": licenza.data_attivazione,
            "data_scadenza": licenza.data_scadenza,
            "scaduta": licenza.scaduta,
            "proprietario": licenza.proprietario
        })

        return str(result.inserted_id)

    def findLicenzaByProprietario(id: str) -> Licenza:
        '''
        Questo metodo trova una licenza non scaduta sul database, usando l'identificativo del suo proprietario

        Parametri
        ----------
        id: str
            id del Proprietario

        Returns
        -------
        licenzaTrovato : licenza
            Restituisce la licenza appena trovata 
        '''
        
        trovato = licenze.find_one({"proprietario": id, "scaduta": False})

        id = str(trovato.get("_id"))
        tipo = trovato.get("tipo")
        costo = trovato.get("costo")
        data_attivazione = trovato.get("data_attivazione")
        data_scadenza = trovato.get("data_scadenza")
        scaduta = trovato.get("scaduta")
        proprietario = trovato.get("proprietario")

        licenzaTrovata = Licenza(
            id,
            tipo,
            costo,
            data_attivazione,
            data_scadenza,
            scaduta,
            proprietario)

        return licenzaTrovata

    def eliminaLicenza(id : str)->bool:
        '''
            Questo metodo prende in ingresso un id ed elimina
            la corrispondente licenza dal database
        '''
            
        result = licenze.delete_one({"_id": ObjectId(id)})
        if(result.deleted_count == 1):
            return True
        else:
            return False

    def modificaLicenza(licenza : Licenza):
    
        trovato = LicenzaDAO.findLicenza(licenza.id)
        if(trovato is None):
            return None
        
        licenze.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "tipo" : licenza.tipo,
        }})
