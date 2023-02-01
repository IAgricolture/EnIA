from src.dbConnection import impianti
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from flask import jsonify
from bson.objectid import ObjectId


class ImpiantoDiIrrigazioneDAO():
    '''
    Classe DAO di Impianto di Irrigazione 

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    findImpiantiByTerreno(idTerreno: str):
        Questo metodo trova tutti gli impiati di irrigazioni associati a id del terreno 
    findImpiantoById(id: str):
        Questo metodo trova un Impianto di irrigazione sul database, usando il suo ObjectId
    creaImpianto(impianto: ImpiantoDiIrrigazione, idTerreno: str)        
        Questo metodo instanzia un impianto di irrigazione sul database
    modificaImpianto(impianto: ImpiantoDiIrrigazione):
        Questo metodo permette la modifica di un impianto di irrigazione sul database
    attivaImpianto(id: str):
        Questo metodo attiva un impianto di irrigazione sul database tramite il suo id 
    disattivaImpianto(id: str):
        Questo metodo disattiva un impianto di irrigazione sul database tramite il suo id 
    eliminaImpianto(id: str):
        Questo metodo elimina un impianto di irrigazione sul database tramite il suo id 

    '''
    
    def findImpiantiByTerreno(idTerreno: str):
        '''
        Questo metodo trova tutti gli impiati di irrigazioni associati a id del terreno 

        Parametri
        ----------
        idTerreno: str
            id del Terreno

        Returns
        -------
        impiantiTrovato : ImpiantoDiIrrigazione
            Restituisce una lista contenete gli impianti trovati 
        '''
        
        # trova impianti sul database con l'id del terreno
        impiantiTrovati = impianti.find({"terreno": ObjectId(idTerreno)})
        impiantiTrovati = list(impiantiTrovati)

        # cast all objectid to string
        for impianto in impiantiTrovati:
            impianto["_id"] = str(impianto["_id"])
            impianto["terreno"] = str(impianto["terreno"])

        return list(impiantiTrovati)

    def findImpiantoById(id: str) -> ImpiantoDiIrrigazione:
        '''
        Questo metodo trova un Impianto di irrigazione sul database, usando il suo ObjectId

        Parametri
        ----------
        id: str
            id del Impianto

        Returns
        -------
        impiantoTrovato : ImpiantoDiIrrigazione
            Restituisce l'occorenza trovata con quell id 
        '''
        trovato = impianti.find_one({"_id": ObjectId(id)})

        id = str(trovato.get("_id"))
        nome = str(trovato.get("nome"))
        tipo = str(trovato.get("tipo"))
        codice = str(trovato.get("codice"))
        attivo = bool(trovato.get("attivo"))
        posizione = trovato.get("posizione")

        impiantoTrovato = ImpiantoDiIrrigazione(
            id, nome, tipo, codice, posizione, attivo)

        return impiantoTrovato

    def creaImpianto(impianto: ImpiantoDiIrrigazione, idTerreno: str) -> str:
        '''
        Questo metodo instanzia un impianto di irrigazione sul database

        Parametri
        ----------
        idTerreno: str
            id del Terreno
        Impianto: ImpiantoDiIrrigazione
            istanza da craeare nel DataBase

        Returns
        -------
        result : str
            Restituisce l'id del impianto appena craeato 
        '''

        result = impianti.insert_one({
            "nome": impianto.nome,
            "tipo": impianto.tipo,
            "codice": impianto.codice,
            "attivo": impianto.attivo,
            "posizione": impianto.posizione,
            "terreno": ObjectId(idTerreno)
        })

        return str(result.inserted_id)

    def modificaImpianto(impianto: ImpiantoDiIrrigazione):
        '''
        Questo metodo permette la modifica di un impianto di irrigazione sul database

        Parametri
        ----------
        impianto: ImpiantoDiIrrigazione
            istanza su cui effetuare la modifica

        Returns
        -------
        '''
        impianti.update_one(
            {"_id": ObjectId(impianto.id)},
            {
                "$set": {
                    "nome": impianto.nome,
                    "tipo": impianto.tipo,
                    "codice": impianto.codice,
                    "attivo": impianto.attivo,
                    "posizione": impianto.posizione
                }
            }
        )

    def attivaImpianto(id: str):
        '''
        Questo metodo attiva un impianto di irrigazione sul database tramite il suo id

        Parametri
        ----------
        id: str
            id del Impianto da attivare 

        Returns
        -------
        Result : int
            Restituisce un valore intero per il controllo
        '''
        result = impianti.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "attivo": True
                }
            }
        )
        # se non è stato trovato nessun impianto con quell'id
        return result.modified_count == 1

    def disattivaImpianto(id: str):
        '''
        Questo metodo disattiva un impianto di irrigazione sul database tramite il suo id

        Parametri
        ----------
        id: str
            id del Impianto da disattivare 

        Returns
        -------
        Result : int
            Restituisce un valore intero per il controllo
        '''
        result = impianti.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "attivo": False
                }
            }
        )
        # se non è stato trovato nessun impianto con quell'id
        return result.modified_count == 1

    def eliminaImpianto(id: str):
        '''
        Questo metodo elimina un impianto di irrigazione sul database tramite il suo id

        Parametri
        ----------
        id: str
            id del Impianto da eliminare

        Returns
        -------
        '''
        impianti.delete_one({"_id": ObjectId(id)})
