
from src.dbConnection import utenti
from src.logic.model.Utente import Utente
from flask import jsonify
import datetime
from bson.objectid import ObjectId

class AutenticazioneDAO():

    def trovaUtenteByEmail(email: str) -> Utente:
        """
            This method find one user in the database, using his email
            :return: Utente
        """
        trovato = utenti.find_one({"email" : email})
        if(trovato == None):
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
        utenteTrovato = Utente(id, nome, cognome, email, password, ruolo, dataNascita, partitaIVA, codice, indirizzo, datore)
        return utenteTrovato

    def trovaUtente(id : str) -> Utente:
        """
            This method find one user in the database, using his ObjectId
            :return: Utente
        """
        trovato = utenti.find_one({"_id" : ObjectId(id)})
        if trovato == None:
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
        utenteTrovato = Utente(id, nome, cognome, email, password, ruolo, dataNascita, partitaIVA, codice, indirizzo, datore)
        return utenteTrovato
        

    def trovaUtenteByCodiceDiAccesso(codice: str) -> Utente:
        """
            This method find one user in the database, using his codiceDiAccesso
            :return: Utente
        """
        trovato = utenti.find_one({"codice" : codice, "ruolo": {"$ne": "farmer"}})
        
        if trovato == None:
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
        utenteTrovato = Utente(id, nome, cognome, email, password, ruolo, dataNascita, partitaIVA, codice, indirizzo, datore)
        return utenteTrovato
    
    def creaUtente(utente : Utente) -> str:
        """
            This method instantiate one utente on the database
        """
        if utente.ruolo == "farmer":
            result = utenti.insert_one({
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "partitaIVA": utente.partitaIVA,
                "indirizzo": utente.indirizzo,
            })
        else:
            result = utenti.insert_one({
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "codice": utente.codice,
                "indirizzo": utente.indirizzo,
                "datore": utente.datore,
            })

        return str(result.inserted_id)


    def eliminaUtente(id : str):
        """
            Questo metodo prende in ingresso un id ed elimina
            il corrispondente utente dal database
        """
        utenti.delete_one({"_id": ObjectId(id)})
    
    def modificaUtente(utente : Utente): 
        """
            Questo metodo prende in ingresso un oggetto utente e lo modifica nel database
        """  
        trovato = AutenticazioneDAO.trovaUtente(str(utente.id))
        if(trovato == None):
            return None

        if utente.ruolo == "farmer":
            return utenti.update_one({"_id": ObjectId(trovato.id)},
            {"$set": {
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "partitaIVA": utente.partitaIVA,
                "indirizzo": utente.indirizzo,
            }})
        else:
            return utenti.update_one({"_id": ObjectId(trovato.id)},
            {"$set": {
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "codice": utente.codice,
                "indirizzo": utente.indirizzo,
                "datore": utente.datore,
            }})


    def listaUtentiTutti():
        """
            Questo metodo restituisce una lista di tutte le entry di utente presenti sul database
        """
        return utenti.find()
    
    def listaDipendenti(datore: str)-> list: 
        return list(utenti.find({"datore": datore}))
        
        





