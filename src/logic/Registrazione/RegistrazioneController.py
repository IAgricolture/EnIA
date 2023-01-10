import hashlib
import json
from src.logic.model.Utente import Utente

from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.model.Licenza import Licenza
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from datetime import timedelta
from datetime import datetime

from flask import jsonify, request, render_template, session, redirect
from src import app
from flask_login import current_user, login_user
from flask import url_for

class RegistrazioneController():
    @app.route("/register", methods = ["GET", "POST"])
    def registrazioneConCodiceDiAccesso():
        if request.method == "POST": 
            richiesta = request.form
            email = richiesta.get("email")
            nome = richiesta.get("nome")
            cognome = richiesta.get("cognome")
            password = hashlib.sha512(richiesta.get("password").encode()).hexdigest()
            dataDiNascita = richiesta.get("dataNascita")
            codiceDiAccesso = richiesta.get("codice")
            #TODO: Implementare la verifica dell'indirizzo
            indirizzo = richiesta.get("indirizzo")
            slotUtente = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codiceDiAccesso)
            risposta = {
                    "emailUsata": False,
                    "codiceNonValido": False,
                    "utenteRegistrato" : False
            }

            #Se l'email è già usata il server avviserà il front-end
            if AutenticazioneDAO.trovaUtenteByEmail(email) != None:
                risposta["emailUsata"] = True
                #Se il codice è già usato oppure non è valido il server avviserà il front end
            elif slotUtente == None or slotUtente.nome != None:
                risposta["codiceNonValido"] = True
                #Altrimenti si recupera lo slot Utente dal database lo si modifica con i dati utente
            else:
                slotUtente.nome = nome
                slotUtente.cognome = cognome
                slotUtente.password = password
                slotUtente.email = email
                slotUtente.dataNascita = dataDiNascita
                slotUtente.indirizzo = indirizzo
                AutenticazioneDAO.modificaUtente(slotUtente)
                risposta["utenteRegistrato"] = True 
                return jsonify(risposta)
        else:
            return render_template("register.html")
                
        @app.route("/registerf", methods = ["GET", "POST"])
        def registrazioneFarmer():
            if request.method == "POST": 
                richiesta = request.form
                email = richiesta.get("email")
                nome = richiesta.get("nome")
                cognome = richiesta.get("cognome")
                password = hashlib.sha512(richiesta.get("password").encode()).hexdigest()
                dataDiNascita = richiesta.get("dataNascita")
                partitaiva = richiesta.get("partitaiva")
                licenza = richiesta.get("licenza")
                numerocarta = richiesta.get("numerocarta")
                titolare = richiesta.get("titolare")
                scadenza = richiesta.get("scadenza")
                cvv = richiesta.get("cvv") 
                #TODO: Implementare la verifica dell'indirizzo
                indirizzo = richiesta.get("indirizzo")
                risposta = {
                    "emailUsata": False
                }

                #Se l'email è già usata il server avviserà il front-end
                if AutenticazioneDAO.trovaUtenteByEmail(email) != None:
                    risposta["emailUsata"] = True
                else:
                    utente = Utente("", nome, cognome, email, password, "farmer", dataDiNascita, partitaiva, None, indirizzo)
                    id = AutenticazioneDAO.creaUtente(utente)
                    #TODO decidere i parametri delle licenze
                    l = Licenza("", licenza, 5000, datetime.now().date().isoformat(), datetime.now().date().isoformat(), False, id)
                    LicenzaDAO.creaLicenza(l)
                    m = MetodoDiPagamento("", numerocarta, titolare, scadenza, cvv, id)
                    MetodoDiPagamentoDAO.creaMetodo(m)

                    return render_template("login.html")
            
            return render_template("registerfarmer.html")
