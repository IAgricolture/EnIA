import hashlib

from src.logic.Registrazione.RegistrazioneService import RegistrazioneService
from src.logic.GestionePagamento.GestionePagamentoService import GestionePagamentoService
from flask import jsonify, request, render_template, redirect
from src import app


class RegistrazioneController():
    '''
    Classe Controller di Registrazione

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    registrazioneConCodiceDiAccesso():
        Permette di effettuare la registrazione di un dipendente tramite codice di accesso
    registrazioneFarmer():
        Permette di effettuare la registrazione da parte del farmer
    '''
    @app.route("/register", methods=["GET", "POST"])
    def registrazioneConCodiceDiAccesso():
        '''Permette di effettuare la registrazione di un dipendente tramite codice di accesso'''
        if request.method == "POST":
            richiesta = request.form
            email = richiesta.get("email")
            nome = richiesta.get("nome")
            cognome = richiesta.get("cognome")
            password = richiesta.get("password")
            dataDiNascita = richiesta.get("dataNascita")
            codiceDiAccesso = richiesta.get("codice")
            indirizzo = richiesta.get("indirizzo")
            risposta = RegistrazioneService.creaUtente(nome, cognome, email, password, dataDiNascita, codiceDiAccesso, indirizzo)
            return jsonify(risposta)
        else:
            return render_template("register.html")

    @app.route("/registerf", methods=["GET", "POST"])
    def registrazioneFarmer():
        '''Permette di effettuare la registrazione da parte del farmer'''
        if request.method == "POST":
            richiesta = request.form
            email = richiesta.get("email")
            nome = richiesta.get("nome")
            cognome = richiesta.get("cognome")
            password = hashlib.sha512(
                richiesta.get("password").encode()).hexdigest()
            dataDiNascita = richiesta.get("dataNascita")
            partitaiva = richiesta.get("partitaiva")
            licenza = richiesta.get("licenza")
            numerocarta = richiesta.get("numerocarta")
            titolare = richiesta.get("titolare")
            scadenza = richiesta.get("scadenza")
            cvv = richiesta.get("cvv") 
            indirizzo = richiesta.get("indirizzo")
            risposta = {
                "emailUsata": False
            }
            # Se l'email è già usata il server avviserà il front-end
            if RegistrazioneService.trovaUtenteByEmail(email) is not None:
                risposta["emailUsata"] = True
            else:
                id = RegistrazioneService.creaFarmer(nome,cognome, email, password, dataDiNascita, partitaiva, indirizzo)
                l = RegistrazioneService.creaLicenza(id, licenza)
                m = GestionePagamentoService.creaMetodoDiPagamento(numerocarta, titolare, scadenza, cvv, id)

                return redirect("/login")
        return render_template("registerfarmer.html")
