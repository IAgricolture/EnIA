import hashlib

from src.logic.Registrazione.RegistrazioneService import RegistrazioneService

from flask import jsonify, request, render_template
from src import app

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
            risposta = RegistrazioneService.modificaUtente(nome, cognome, email, password, dataDiNascita, codiceDiAccesso, indirizzo)
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
            tipo = richiesta.get("licenza")
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
            if RegistrazioneService.trovaUtenteByEmail(email) != None:
                risposta["emailUsata"] = True
            else:
                id = RegistrazioneService.creaFarmer(nome,cognome, email, password, dataDiNascita, partitaiva, indirizzo)
                #TODO decidere i parametri delle licenze
                l = RegistrazioneService.creaLicenza(id, tipo)
                m = RegistrazioneService.creaMetodoDiPagamento(numerocarta, titolare, scadenza, cvv, id)

                return render_template("login.html")
        else:
            return render_template("registerfarmer.html")

