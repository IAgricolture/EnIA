
from src.dbConnection import utenti
from src.logic.model.Utente import Utente
from flask import jsonify
import datetime
from bson.objectid import ObjectId

class UtenteDAO():

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
        utenteTrovato = Utente(id, nome, cognome, email, ruolo, dataNascita, codice, indirizzo, password, partitaIVA)
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
        utenteTrovato = Utente(id, nome, cognome, email, ruolo, dataNascita, codice, indirizzo, password, partitaIVA)
        return utenteTrovato
        

    def trovaUtenteByCodiceDiAccesso(codice: str) -> Utente:
        """
            This method find one user in the database, using his codiceDiAccesso
            :return: Utente
        """
        trovato = utenti.find_one({"codice" : codice})
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
        utenteTrovato = Utente(id, nome, cognome, email, ruolo, dataNascita, codice, indirizzo, password, partitaIVA)
        return utenteTrovato
    
    def creaUtente(utente : Utente):
        """
            This method instantiate one utente on the database
        """
        if utente.ruolo == "farmer":
            utenti.insert_one({
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
            utenti.insert_one({
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "codice": utente.codice,
                "indirizzo": utente.indirizzo,
            })


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
        trovato = UtenteDAO.trovaUtente(str(utente.id))
        if(trovato == None):
            return None

        if utente.ruolo == "farmer":
            utenti.update_one({"_id": ObjectId(trovato.id)},
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
            utenti.update_one({"_id": ObjectId(trovato.id)},
            {"$set": {
                "nome" : utente.nome,
                "cognome": utente.cognome,
                "email": utente.email,
                "password": utente.password,
                "ruolo": utente.ruolo,
                "dataNascita" : utente.dataNascita,
                "codice": utente.codice,
                "indirizzo": utente.indirizzo,
            }})


    def listaUtentiTutti():
        """
            Questo metodo restituisce una lista di tutte le entry di utente presenti sul database
        """
        return utenti.find()




