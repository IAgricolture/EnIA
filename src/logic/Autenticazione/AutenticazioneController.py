from src import login_manager

from src.logic.Autenticazione import AutenticazioneService

from flask import request, render_template, redirect
from src import app

class AutenticazioneController():
    #This method is mandatory to use the flask_login module
    @login_manager.user_loader
    def load_user(user_id):
        """
            This method tells flask how to load a user from its session using an unique id
            :return: Utente
        """
        return AutenticazioneService.trovaUtenteByEmail()

    @app.route("/login", methods = ["GET", "POST"])
    def login():
        """
        Reads the users credentials from a https request if they match with one entry
        on the database, the system change his state from anonymous to logged user
        :return: redirect to index page
        """
        if request.method == "POST" :
            email = request.form.get("email")
            password = request.form.get("password")
            successo = AutenticazioneService.login()
            if successo:
                return redirect("user")
            else:
                return render_template("login.html")        
        else:
            return render_template("login.html")

