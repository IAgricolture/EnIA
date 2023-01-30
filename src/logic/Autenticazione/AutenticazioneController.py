from src import login_manager

from src.logic.Autenticazione.AutenticazioneService import AutenticazioneService

from flask import request, render_template, redirect, url_for
from src import app


class AutenticazioneController():
    '''
    Classe Controller di Autenticazione

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    load_user(user_id):
        Carica un utente dalla sessione utilizzando il suo id univoco
    login():
        Controlla le credenziali inserite dall'utente, se c'è una corrispondenza sul database il sistema
        cambia il suo stato da anonimo ad utente loggato
    logout():
        Effettua il logout di un utente

    '''
    # This method is mandatory to use the flask_login module
    @login_manager.user_loader
    def load_user(user_id):
        '''Carica un utente dalla sessione utilizzando il suo id univoco'''
        return AutenticazioneService.trovaUtenteById(user_id)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        '''Controlla le credenziali inserite dall'utente, se c'è una corrispondenza
        sul database il sistema cambia il suo stato da anonimo ad utente loggato'''
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            urlLastPage = request.form.get("next")
            redirectUrl = "visualizzaTerreni"
            successo = AutenticazioneService.login(email, password)
            if successo:
                # Se ha provato ad accedere ad una pagina prima di arrivare al
                # login automaticamente:
                if (urlLastPage):
                    redirectUrl = urlLastPage
                return redirect(redirectUrl)
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")

    @app.route("/logout")
    def logout():
        '''Effettua il logout di un utente'''
        AutenticazioneService.logout()
        # Uso url_for per generare un url valido per login: render_template
        # copia nell'url logout, che per qualche motivo crea problemi con il
        # redirect.
        return redirect(url_for("login"))
