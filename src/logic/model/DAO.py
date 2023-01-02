from dbConnection import utenti
from entities import Utente
from flask import jsonify
import datetime

class UtenteDAO():

    def findUtente(id : int) -> Utente:
        return utenti.find(id)

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



#PROVA SUL DATABASE
utente = Utente("Benedetto", "Scala", "ben.scala@libero.it", "password", "farmer", datetime.datetime.now(), "partitaIVA", "codice","Via Molino 13")

UtenteDAO.creaUtente(utente)
