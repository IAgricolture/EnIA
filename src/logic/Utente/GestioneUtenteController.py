import hashlib
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from src.logic.Utente.GestioneUtenteService import GestioneUtenteService
from src.logic.GestionePagamento.GestionePagamentoService import GestionePagamentoService
from src.logic.model.Licenza import Licenza

from flask import request, render_template, session, jsonify
from src import app
from flask_login import current_user, login_required

class GestioneUtenteController():
    @app.route("/user", methods = ["GET", "POST"])
    def user():
        if request.method == "POST":
            richiesta = request.form
            tipo = richiesta.get("type")
            if tipo == "user":
                current_user.nome = richiesta.get("nome")
                current_user.cognome = richiesta.get("cognome")
                current_user.email = richiesta.get("email")
                current_user.dataNascita = richiesta.get("dataNascita")
                current_user.indirizzo = richiesta.get("indirizzo")
                print(richiesta.get("password")!= None)
                if richiesta.get("password") != None:
                    current_user.password = hashlib.sha512(richiesta.get("password").encode()).hexdigest()
                if current_user.ruolo == "farmer":
                    current_user.partitaiva = richiesta.get("partitaIVA")
                
                GestioneUtenteService.modificaUtente(current_user)
            elif tipo == "licenza":
                licenza = Licenza(**session["licenza"])
                nuovotipo = richiesta.get("tipo")
                GestioneUtenteService.moficicaLicenza(licenza,nuovotipo)
            elif tipo == "metodo":
                mp = MetodoDiPagamento(**session["metodo"])
                num_carta = richiesta.get("num_carta")
                titolare = richiesta.get("titolare")
                scadenza = richiesta.get("scadenza")
                cvv = richiesta.get("cvv")
                GestionePagamentoService.modificaMetodo(mp, num_carta, titolare, scadenza, cvv)
                
        if current_user.ruolo == "farmer":
            session["licenza"] = GestioneUtenteService.findLicenzaByProprietario(current_user.id).__dict__
            session["metodo"] = GestionePagamentoService.findMetodoByProprietario(current_user.id).__dict__
        return render_template("user.html")
        
    @app.route("/AziendaAgricola", methods = ["GET", "POST"])
    @login_required
    def aziendaagricola():
        if request.method == "POST":
            richiesta = request.form
            tipo = richiesta.get("type")
        listdipendenti = GestioneUtenteService.getUtenti(current_user.id)
        for i in listdipendenti: 
            i["_id"]= str(i["_id"])
        session["dipendenti"]= listdipendenti
        return render_template("AziendaAgricola.html")
    
    @app.route("/removeFromAzienda", methods = ["POST"])
    def removeFromAzienda():
        richiesta = request.get_json()
        print(richiesta)
        id = richiesta.get("id")
        if(GestioneUtenteService.removeUtenteFromAzienda(id)):
            result = "True"
        else:
            result = "False"
        message = {
            "result": result
        }
        return jsonify(message)
        

    @app.route("/GenCode", methods = ["GET", "POST"])
    def GenCode():
        if request.method == "POST":
            richiesta = request.form
            ruolo = richiesta.get("ruolo")
            datore = richiesta.get("datore")
            codice = GestioneUtenteService.GenerateCode(ruolo, datore)
            return jsonify(codice)