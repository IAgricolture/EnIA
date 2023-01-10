from src import login_manager
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

class AutenticazioneController():
    #This method is mandatory to use the flask_login module
    @login_manager.user_loader
    def load_user(user_id):
        """
            This method tells flask how to load a user from its session using an unique id
            :return: Utente
        """
        return AutenticazioneDAO.trovaUtente(user_id)

    @app.route("/login", methods = ["GET", "POST"])
    def login():
        """
        Reads the users credentials from a https request if they match with one entry
        on the database, the system change his state from anonymous to logged user
        :return: redirect to index page
        """
        if request.method == "POST" :
            successo = False
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            login_attempt : Utente = AutenticazioneDAO.trovaUtenteByEmail(email)

            if not login_attempt:
                print("Utente non registrato")
                successo = False
            
            if login_attempt.password == hashed_password:
                login_user(login_attempt, duration=timedelta(days=365), force=True)
                successo = True
                
            else:
                print("password errata")
                successo = False

            if successo:
                return redirect("user")
            else:
                return render_template("login.html")        
        else:
            return render_template("login.html")

