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
                if current_user.ruolo == "farmer":
                    current_user.partitaiva = richiesta.get("partitaIVA")
                
                AutenticazioneDAO.modificaUtente(current_user)
            elif tipo == "licenza":
                #TODO decidere come far avvenire il cambio licenza
                print(richiesta.get("licenza"))
            elif tipo == "metodo":
                metodo = MetodoDiPagamento(**session["metodo"])
                
                metodo.num_carta = richiesta.get("num_carta")
                metodo.titolare = richiesta.get("titolare")
                metodo.scadenza = richiesta.get("scadenza")
                metodo.cvv = richiesta.get("cvv")
        
                MetodoDiPagamentoDAO.modificaMetodo(metodo)
                
        if current_user.ruolo == "farmer":
            session["licenza"] = LicenzaDAO.findLicenzaByProprietario(current_user.id).__dict__
            session["metodo"] = MetodoDiPagamentoDAO.findMetodoByProprietario(current_user.id).__dict__
        return render_template("user.html")
        

        

        
        

