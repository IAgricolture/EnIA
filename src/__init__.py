from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'jshwifhjwieoajhf5847f5ae4eaws'
login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
login_manager.login_message_category = "info"

from src.logic.GestioneUtente import GestioneUtenteAuth


from src import routes
from src.logic.GestioneUtente import GestioneUtenteControl
