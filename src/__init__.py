

from flask import Flask, redirect, render_template, url_for, flash
from flask_login import LoginManager, current_user
from flask_cors import CORS






"""
   This file represents our app, it is from this file that our application starts,
   and it is from this file only that we call all the other modules
   such as routes, or gestioneUtenteControl
"""
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://enia:vp7CMyN7V5Rl8FZR@ac-raqtab6-shard-00-00.o0m35vt.mongodb.net:27017,ac-raqtab6-shard-00-01.o0m35vt.mongodb.net:27017,ac-raqtab6-shard-00-02.o0m35vt.mongodb.net:27017/EnIA?ssl=true&replicaSet=atlas-6sol94-shard-0&authSource=admin&retryWrites=true&w=majority"
app.config["COMPRESS_ALGORITHM"] = 'gzip'  # disable default compression of all eligible requests
app.config['SECRET_KEY'] = 'jshwifhjwieoajhf5847f5ae4eaws'
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from functools import wraps

def farmer_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.ruolo == "farmer":
            return f(*args, **kwargs)
        else:
            flash("Devi essere un farmer per vedere questa pagina.", 'error')
            return render_template('error-404.html')

    return wrap

from src import routes
from src.logic.Autenticazione import AutenticazioneController
from src.logic.Registrazione import RegistrazioneController
from src.logic.Utente import GestioneUtenteController
from src.logic.AmbienteAgricolo import AmbienteAgricoloController
from src.logic.DecisionIntelligence import DecisionIntelligenceController
from src.logic.GestioneEventi import GestioneEventiController, GestioneEventiService
from src.logic.GestionePagamento import GestionePagamentoController
from src.logic.AmbienteAgricolo import GestioneScheduleController