
from src.dbConnection import utenti
from src.logic.model.Utente import Utente
from flask import jsonify
import datetime
from bson.objectid import ObjectId


class AutenticazioneDAO():
    
    '''
    Classe DAO di Autenticazione

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    trovaUtenteByEmail(email: str):
        Questo metodo trova un utente nel database, utilizzando la sua email
    trovaUtente(id: str):
        Questo metodo trova un utente nel database, utilizzando il suo ObjectId
    trovaUtenteByCodiceDiAccesso(codice: str):        
        Questo metodo trova un utente nel database, utilizzando il suo codiceDiAccesso
    creaUtente(utente: Utente):
        Questo metodo permette di istanziare un utente sul database
    eliminaUtente(id: str):
        Questo metodo prende in ingresso un id ed elimina il corrispondente utente dal database
    modificaUtente(id: str):
         Questo metodo prende in ingresso un oggetto utente e lo modifica nel database
    listaUtentiTutti():
        Questo metodo restituisce una lista di tutte le entry di utente presenti sul database
    listaDipendenti(datore: str):
        Questo metodo restituisce una lista di tutte le entry dei dipendenti relativi ad un datore di lavoro
    insertSlot(ruolo: str, codice: str, datore: str):
        Questo metodo permette al datore di settare il ruolo ad un dipendete 
    getDatore(codice: str):
        Questo metodo permette di ottenere il datore il lavoro avendo un codice

    '''
    
    def trovaUtenteByEmail(email: str) -> Utente:
        '''
        Questo metodo trova un utente nel database, utilizzando la sua email

        Parametri
        ----------
        email : str
            email del utente

        Returns
        -------
        utenteTrovato : utente
            Restituisce l'utente desiderato
        '''
        trovato = utenti.find_one({"email": email})
        if (trovato is None):
            return None
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        cognome = trovato.get("cognome")
        email = trovato.get("email")
        ruolo = trovato.get("ruolo")
        dataNascita = trovato.get("dataNascita")
        codice = trovato.get("codice")
        indirizzo = trovato.get("indirizzo")
        password = trovato.get("password")
        partitaIVA = trovato.get("partitaIVA")
        datore = trovato.get("datore")
        utenteTrovato = Utente(
            id,
            nome,
            cognome,
            email,
            password,
            ruolo,
            dataNascita,
            partitaIVA,
            codice,
            indirizzo,
            datore)
        return utenteTrovato

    def trovaUtente(id: str) -> Utente:
        '''
        Questo metodo trova un utente nel database, utilizzando il suo ObjectId

        Parametri
        ----------
        id: str
            id del Utente

        Returns
        -------
        utenteTrovato : utente
            Restituisce l'utente desiderato
        '''
        trovato = utenti.find_one({"_id": ObjectId(id)})
        if trovato is None:
            return None
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        cognome = trovato.get("cognome")
        email = trovato.get("email")
        ruolo = trovato.get("ruolo")
        dataNascita = trovato.get("dataNascita")
        codice = trovato.get("codice")
        indirizzo = trovato.get("indirizzo")
        password = trovato.get("password")
        partitaIVA = trovato.get("partitaIVA")
        datore = trovato.get("datore")
        utenteTrovato = Utente(
            id,
            nome,
            cognome,
            email,
            password,
            ruolo,
            dataNascita,
            partitaIVA,
            codice,
            indirizzo,
            datore)
        return utenteTrovato

    def trovaUtenteByCodiceDiAccesso(codice: str) -> Utente:
        '''
        Questo metodo trova un utente nel database, utilizzando il suo codiceDiAccesso

        Parametri
        ----------
        codice : str
            codice univoco del dipendente

        Returns
        -------
        utenteTrovato : utente
            Restituisce l'utente desiderato
        None : NoneType
            Nessun utente restituito
        '''
        trovato = utenti.find_one(
            {"codice": codice, "ruolo": {"$ne": "farmer"}})

        if trovato is None:
            return None
        id = str(trovato.get("_id"))
        nome = trovato.get("nome")
        cognome = trovato.get("cognome")
        email = trovato.get("email")
        ruolo = trovato.get("ruolo")
        dataNascita = trovato.get("dataNascita")
        codice = trovato.get("codice")
        indirizzo = trovato.get("indirizzo")
        password = trovato.get("password")
        partitaIVA = trovato.get("partitaIVA")
        datore = trovato.get("datore")
        utenteTrovato = Utente(
            id,
            nome,
            cognome,
            email,
            password,
            ruolo,
            dataNascita,
            partitaIVA,
            codice,
            indirizzo,
            datore)
        return utenteTrovato

    def creaUtente(utente: Utente) -> str:
        '''
        Questo metodo permette di istanziare un utente sul database

        Parametri
        ----------
        utente: Utente
            Utente da inserire nel DataBase

        Returns
        -------
        result.inserted_id: str
            id del Utente appena inserito
        '''
        if utente.ruolo == "farmer":
            result = utenti.insert_one({
                "nome": utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita": utente.dataNascita,
                "partitaIVA": utente.partitaIVA,
                "indirizzo": utente.indirizzo,
            })
        else:
            result = utenti.insert_one({
                "nome": utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita": utente.dataNascita,
                "codice": utente.codice,
                "indirizzo": utente.indirizzo,
                "datore": utente.datore,
            })

        return str(result.inserted_id)

    def eliminaUtente(id: str):
        '''
        Questo metodo prende in ingresso un id ed elimina il corrispondente utente dal database

        Parametri
        ----------
        id : str
            id del Utente

        Returns
        -------
        True : bool
            Valore Booleano per avvenuta cancellazione
        '''
        return utenti.delete_one({"_id": ObjectId(id)})

    def modificaUtente(utente: Utente):
        '''
        Questo metodo prende in ingresso un oggetto utente e lo modifica nel database

        Parametri
        ----------
        utente: Utente
            Utente da modificare

        Returns
        -------
        True : bool
            Modifica avvenuta con successo
        '''
        trovato = AutenticazioneDAO.trovaUtente(str(utente.id))
        if (trovato is None):
            return None

        if utente.ruolo == "farmer":
            return utenti.update_one({"_id": ObjectId(trovato.id)},
                                     {"$set": {
                                         "nome": utente.nome,
                                         "cognome": utente.cognome,
                                         "email": utente.email,
                                         "password": utente.password,
                                         "ruolo": utente.ruolo,
                                         "dataNascita": utente.dataNascita,
                                         "partitaIVA": utente.partitaIVA,
                                         "indirizzo": utente.indirizzo,
                                     }})
        else:
            return utenti.update_one({"_id": ObjectId(trovato.id)},
                                     {"$set": {
                                         "nome": utente.nome,
                                         "cognome": utente.cognome,
                                         "email": utente.email,
                                         "password": utente.password,
                                         "ruolo": utente.ruolo,
                                         "dataNascita": utente.dataNascita,
                                         "codice": utente.codice,
                                         "indirizzo": utente.indirizzo,
                                         "datore": utente.datore,
                                     }})

    def listaUtentiTutti():
        '''
        Questo metodo restituisce una lista di tutte le entry di utente presenti sul database

        Parametri
        ----------
        
        Returns
        -------
        utenti : Utente
            Lista di utenti
        '''
        return utenti.find()

    def listaDipendenti(datore: str) -> list:
        '''
        Questo metodo restituisce una lista di tutte le entry dei dipendenti relativi ad un datore di lavoro

        Parametri
        ----------
        datore : str
            datore di lavore del dipendente

        Returns
        -------
        utenti : Utente
            Lista di dipendenti relativi a quel datore
        '''
        return list(utenti.find({"datore": datore}))

    def insertSlot(ruolo: str, codice: str, datore: str):
        '''
        Questo metodo permette al datore di settare il ruolo ad un dipendete

        Parametri
        ----------
        ruolo : str
            ruolo del dipendete
        codice: str
            codice del dipendete
        datore: str
            datore del dipendente

        Returns
        -------
        '''
        utenti.insert_one({
            "nome": "",
            "cognome": "",
            "email": "",
            "password": "",
            "ruolo": ruolo,
            "dataNascita": "",
            "codice": codice,
            "indirizzo": "",
            "datore": datore,
        })

    def getDatore(codice: str) -> str:
        '''
        Questo metodo permette di ottenere il datore il lavoro avendo un codice

        Parametri
        ----------
        codice : str
            codice del dipendente

        Returns
        -------
        utente : Utente
            lista di dipendenti con quel datore
        '''
        return utenti.find_one({"_id": ObjectId(codice)}).get("datore")
