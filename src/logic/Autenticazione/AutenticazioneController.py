from src import login_manager

from src.logic.Autenticazione.AutenticazioneService import AutenticazioneService

from flask import request, render_template, redirect, url_for
from src import app

class AutenticazioneController():
    #This method is mandatory to use the flask_login module
    @login_manager.user_loader
    def load_user(user_id):
        """
            This method tells flask how to load a user from its session using an unique id
            :return: Utente
        """
        return AutenticazioneService.trovaUtenteById(user_id)

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
            urlLastPage = request.form.get("next")
            redirectUrl = "visualizzaTerreni"
            successo = AutenticazioneService.login(email, password)
            if successo:
                #Se ha provato ad accedere ad una pagina prima di arrivare al login automaticamente:
                if(urlLastPage):
                    redirectUrl = urlLastPage
                return redirect(redirectUrl)
            else:
                return render_template("login.html")        
        else:
            return render_template("login.html")

    @app.route("/logout")
    def logout():
        AutenticazioneService.logout()
        return redirect(url_for("login")) #Uso url_for per generare un url valido per login: render_template copia nell'url logout, che per qualche motivo crea problemi con il redirect.