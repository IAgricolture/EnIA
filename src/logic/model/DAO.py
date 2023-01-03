
from src.logic.model.dbConnection import utenti
from src.logic.model.entities import Utente
from flask import jsonify
import datetime
from bson.objectid import ObjectId

class UtenteDAO():

    def findUtenteByEmail(email: str) -> Utente:
        trovato = utenti.find_one({"email" : email})
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
        return utenteTrovato

    def findUtente(id : str):
        trovato = utenti.find_one({"_id" : ObjectId(id)})
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
        return utenteTrovato
        

    
    def creaUtente(utente : Utente):
        utenti.insert_one({
            "nome" : utente.nome,
            "cognome": utente.cognome,
            "email": utente.email,
            "password": utente.password,
            "ruolo": utente.ruolo,
            "dataNascita" : str(utente.dataNascita),
            "partitaIVA": utente.partitaIVA,
            "codice": utente.codice,
            "indirizzo": utente.indirizzo
        })



