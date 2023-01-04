
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
        utenteTrovato = Utente()
        utenteTrovato.id = str(trovato.get("_id"))
        utenteTrovato.nome = trovato.get("nome")
        utenteTrovato.cognome = trovato.get("cognome")
        utenteTrovato.email = trovato.get("email")
        utenteTrovato.ruolo = trovato.get("ruolo")
        utenteTrovato.dataNascita = trovato.get("dataNascita")
        utenteTrovato.codice = trovato.get("codice")
        utenteTrovato.indirizzo = trovato.get("indirizzo")
        utenteTrovato.password = trovato.get("password")
        utenteTrovato.licenza = str(trovato.get("licenza"))
        utenteTrovato.partitaIVA = trovato.get("partitaIVA")
        return utenteTrovato

    def trovaUtente(id : str) -> Utente:
        """
            This method find one user in the database, using his ObjectId
            :return: Utente
        """
        trovato = utenti.find_one({"_id" : ObjectId(id)})
        if trovato == None:
            return None
        utenteTrovato = Utente()
        utenteTrovato.id = str(trovato.get("_id"))
        utenteTrovato.nome = trovato.get("nome")
        utenteTrovato.cognome = trovato.get("cognome")
        utenteTrovato.email = trovato.get("email")
        utenteTrovato.ruolo = trovato.get("ruolo")
        utenteTrovato.dataNascita = trovato.get("dataNascita")
        utenteTrovato.codice = trovato.get("codice")
        utenteTrovato.indirizzo = trovato.get("indirizzo")
        utenteTrovato.password = trovato.get("password")
        utenteTrovato.licenza = str(trovato.get("licenza"))
        utenteTrovato.partitaIVA = trovato.get("partitaIVA")
        return utenteTrovato
        

    def trovaUtenteByCodiceDiAccesso(codice: str) -> Utente:
        """
            This method find one user in the database, using his codiceDiAccesso
            :return: Utente
        """
        trovato = utenti.find_one({"codice" : codice})
        if trovato == None:
            return None
        utenteTrovato = Utente()
        utenteTrovato.id = str(trovato.get("_id"))
        utenteTrovato.nome = trovato.get("nome")
        utenteTrovato.cognome = trovato.get("cognome")
        utenteTrovato.email = trovato.get("email")
        utenteTrovato.ruolo = trovato.get("ruolo")
        utenteTrovato.dataNascita = trovato.get("dataNascita")
        utenteTrovato.codice = trovato.get("codice")
        utenteTrovato.indirizzo = trovato.get("indirizzo")
        utenteTrovato.password = trovato.get("password")
        utenteTrovato.licenza = str(trovato.get("licenza"))
        utenteTrovato.partitaIVA = trovato.get("partitaIVA")
        return utenteTrovato
    
    def creaUtente(utente : Utente):
        """
            This method instantiate one utente on the database
        """
        utenti.insert_one({
            "nome" : utente.nome,
            "cognome": utente.cognome,
            "email": utente.email,
            "password": utente.password,
            "ruolo": utente.ruolo,
            "dataNascita" : str(utente.dataNascita),
            "partitaIVA": utente.partitaIVA,
            "codice": utente.codice,
            "indirizzo": utente.indirizzo,
            "licenza" : utente.licenza
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
        trovato.nome = utente.nome
        trovato.cognome = utente.cognome
        trovato.dataNascita = utente.dataNascita
        trovato.email = utente.email
        trovato.indirizzo = utente.indirizzo
        trovato.partitaIVA = utente.partitaIVA
        trovato.password = utente.password
        trovato.ruolo = utente.ruolo
        trovato.codice = utente.codice
        trovato.licenza = str(trovato.licenza)
        utenti.update_one({"_id": ObjectId(trovato.id)},
        {"$set": {
            "nome" : utente.nome,
            "cognome": utente.cognome,
            "email": utente.email,
            "password": utente.password,
            "ruolo": utente.ruolo,
            "dataNascita" : str(utente.dataNascita),
            "partitaIVA": utente.partitaIVA,
            "codice": utente.codice,
            "indirizzo": utente.indirizzo,
            "licenza" : utente.licenza
        }})

    def listaUtentiTutti():
        """
            Questo metodo restituisce una lista di tutte le entry di utente presenti sul database
        """
        return utenti.find()




