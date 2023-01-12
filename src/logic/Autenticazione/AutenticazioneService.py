
import hashlib
from src.logic.model.Utente import Utente

from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from datetime import timedelta

from flask_login import login_user

class AutenticazioneService():
    
    def login(email:str, password:str) -> bool:
        successo = False
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        login_attempt : Utente = AutenticazioneDAO.trovaUtenteByEmail(email)
        
        if not login_attempt:
            print("Utente non registrato")
            successo = False
            
        if login_attempt.password == hashed_password:
            login_user(login_attempt, duration=timedelta(days=365), force=True)
            successo = True
                
        else:
            print("password errata")
            successo = False
        
        return successo
    
    def trovaUtenteByEmail(id:str)-> Utente:
        return AutenticazioneDAO.trovaUtenteByEmail(id)
        
