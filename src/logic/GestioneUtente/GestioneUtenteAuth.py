from src import login_manager
from src.logic.model.UtenteDAO import UtenteDAO


#This method is mandatory to use the flask_login module
@login_manager.user_loader
def load_user(user_id):
    """
        This method tells flask how to load a user from its session using an unique id
        :return: Utente
    """
    return UtenteDAO.trovaUtente(user_id)



