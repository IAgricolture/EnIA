import hashlib
from src.logic.model.Utente import Utente

from src.logic.model.UtenteDAO import UtenteDAO
from datetime import timedelta

from flask import jsonify, request, render_template
from src import app
from flask_login import login_user
from flask import url_for

class UtenteControl():
    @app.route("/login", methods = ["GET"])
    def login():
        """
        Reads the users credentials from a https request if they match with one entry
        on the database, the system change his state from anonymous to logged user
        :return: redirect to index page
        """
        print(request.args)
        email = request.args.get("email")
        print(email)
        password = request.args.get("password")
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        login_attempt : Utente = UtenteDAO.trovaUtenteByEmail(email)

        if not login_attempt:
            #TODO:Gestire Errore
            print("Utente non registrato")
            return jsonify({"successo": "false"})
        
        print(login_attempt.password + " e " + hashed_password)
        if login_attempt.password == hashed_password:
            login_user(login_attempt, duration=timedelta(days=365), force=True)
        else:
            #TODO
            print("password errata")
            return jsonify({"successo:": "false"})
        return jsonify({"successo": "true"})