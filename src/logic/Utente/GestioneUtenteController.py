import hashlib
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from src.logic.Utente.GestioneUtenteService import GestioneUtenteService

from flask import request, render_template, session, jsonify
from src import app
from flask_login import current_user, login_required


class GestioneUtenteController():
    '''
    Classe Controller di Gestione Utente

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    user():
        Permette sia la visualizzazione sia la modifica dei dati degli utenti
    aziendaagricola():
        Permette la visualizzazione dei dipendenti di un farmer
    removeFromAzienda():
        Permette la rimozione di un dipendente
    GenCode():
        Permette di generare un codice di accesso per un dipendente
    '''

    @app.route("/user", methods=["GET", "POST"])
    def user():
        '''Permette sia la visualizzazione sia la modifica dei dati degli utenti'''
        if request.method == "POST":
            richiesta = request.form
            tipo = richiesta.get("type")
            if tipo == "user":
                current_user.nome = richiesta.get("nome")
                current_user.cognome = richiesta.get("cognome")
                current_user.email = richiesta.get("email")
                current_user.dataNascita = richiesta.get("dataNascita")
                current_user.indirizzo = richiesta.get("indirizzo")
                print(richiesta.get("password") is not None)
                if richiesta.get("password") is not None:
                    current_user.password = hashlib.sha512(
                        richiesta.get("password").encode()).hexdigest()
                if current_user.ruolo == "farmer":
                    current_user.partitaiva = richiesta.get("partitaIVA")

                GestioneUtenteService.modificaUtente(current_user)
            elif tipo == "licenza":
                # TODO decidere come far avvenire il cambio licenza
                print(richiesta.get("licenza"))
            elif tipo == "metodo":
                mp = MetodoDiPagamento(**session["metodo"])
                num_carta = richiesta.get("num_carta")
                titolare = richiesta.get("titolare")
                scadenza = richiesta.get("scadenza")
                cvv = richiesta.get("cvv")
                GestioneUtenteService.modificaMetodo(
                    mp, num_carta, titolare, scadenza, cvv)

        if current_user.ruolo == "farmer":
            session["licenza"] = GestioneUtenteService.findLicenzaByProprietario(
                current_user.id).__dict__
            session["metodo"] = GestioneUtenteService.findMetodoByProprietario(
                current_user.id).__dict__
        return render_template("user.html")

    @app.route("/AziendaAgricola", methods=["GET", "POST"])
    @login_required
    def aziendaagricola():
        '''Permette la visualizzazione dei dipendenti di un farmer'''
        if request.method == "POST":
            richiesta = request.form
            tipo = richiesta.get("type")
        listdipendenti = GestioneUtenteService.getUtenti(current_user.id)
        for i in listdipendenti:
            i["_id"] = str(i["_id"])
        session["dipendenti"] = listdipendenti
        return render_template("AziendaAgricola.html")

    @app.route("/removeFromAzienda", methods=["POST"])
    def removeFromAzienda():
        '''Permette la rimozione di un dipendente'''
        richiesta = request.get_json()
        print(richiesta)
        id = richiesta.get("id")
        if (GestioneUtenteService.removeUtenteFromAzienda(id)):
            result = "True"
        else:
            result = "False"
        message = {
            "result": result
        }
        return jsonify(message)

    @app.route("/GenCode", methods=["GET", "POST"])
    def GenCode():
        '''Permette di generare un codice di accesso per un dipendente'''
        if request.method == "POST":
            richiesta = request.form
            ruolo = richiesta.get("ruolo")
            datore = richiesta.get("datore")
            codice = GestioneUtenteService.GenerateCode(ruolo, datore)
            return jsonify(codice)
