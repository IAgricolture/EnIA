from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS


"""
   This file represents our app, it is from this file that our application starts,
   and it is from this file only that we call all the other modules
   such as routes, or gestioneUtenteControl
"""
app = Flask(__name__, static_url_path="/templates", static_folder="templates")
CORS(app)
app.config["MONGO_URI"] = "mongodb://enia:vp7CMyN7V5Rl8FZR@ac-raqtab6-shard-00-00.o0m35vt.mongodb.net:27017,ac-raqtab6-shard-00-01.o0m35vt.mongodb.net:27017,ac-raqtab6-shard-00-02.o0m35vt.mongodb.net:27017/EnIA?ssl=true&replicaSet=atlas-6sol94-shard-0&authSource=admin&retryWrites=true&w=majority"
app.config["COMPRESS_ALGORITHM"] = 'gzip'  # disable default compression of all eligible requests
app.config['SECRET_KEY'] = 'jshwifhjwieoajhf5847f5ae4eaws'
login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
login_manager.login_message_category = "info"

from src.logic.GestioneUtente import GestioneUtenteAuth
from src import routes
from src.logic.GestioneUtente import GestioneUtenteControl
from src.logic.GestioneAmbienteAgricolo import GestioneAmbienteAgricoloControl
