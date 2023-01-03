from flask_login import UserMixin

from src import login_manager
from src.logic.model.DAO import UtenteDAO

@login_manager.user_loader
def load_user(user_id):
    return UtenteDAO.findUtente(user_id)



