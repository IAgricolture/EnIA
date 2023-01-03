import hashlib
from src.logic.model.entities import Utente

from src.logic.model.DAO import UtenteDAO
from datetime import timedelta

from flask import request, render_template
from src import app
from flask_login import login_user
from flask import url_for

class UtenteControl():
    @app.route("/login", methods = ["GET", "POST"])
    def login():
        """
        Reads the users credentials from a https request if they match with one entry
        on the database, the system change his state from anonymous to logged user
        :return: redirect to index page
        """
        email = request.form.get("email")
        print(email)
        password = request.form.get("password")
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        login_attempt : Utente = UtenteDAO.findUtenteByEmail(email)

        if not login_attempt:
            #TODO:Gestire Errore
            print("Utente non registrato")
        
        print(login_attempt.password + " e " + hashed_password)
        if login_attempt.password == hashed_password:
            login_user(login_attempt, duration=timedelta(days=365), force=True)
        else:
            #TODO
            print("password errata")
            return render_template("login.html", cssfile=url_for("static",filename = "style.css"))
        return render_template("index.html")