
import hashlib
from src.logic.model.Utente import Utente

from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from datetime import timedelta

from flask_login import login_user, logout_user


class AutenticazioneService():
    '''
    Classe Service di Autenticazione

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    login(email: str, password: str):
        Controlla se le credenziali di accesso sono presenti sul database
    trovaUtenteById(id: str):
        Cerca un utente sul DataBase attraverso il suo id
    logout():
        Effettua il logout
    getDatoreFromDipendente(idDipendente: str):
        Recupera il datore del dipendente

    '''

    def login(email: str, password: str) -> bool:
        '''
        Controlla se le credenziali di accesso sono presenti sul database

        Parametri
        ----------
        email : str
            E-mail
        password : str
            password

        Returns
        -------
        successo : bool
            Esito del login
        '''
        successo = False
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        login_attempt: Utente = AutenticazioneDAO.trovaUtenteByEmail(email)

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

    def trovaUtenteById(id: str) -> Utente:
        '''
        Cerca un utente sul DataBase attraverso il suo id

        Parametri
        ----------
        id : str

        Returns
        -------
        AutenticazioneDAO.trovaUtente(id): Utente
            Utente trovato sul DB
        '''
        return AutenticazioneDAO.trovaUtente(id)

    def logout():
        '''
        Effettua il logout

        Parametri
        ----------
        None

        Returns
        -------
        None
        '''
        logout_user()
        print("Logout utente")

    def getDatoreFromDipendente(idDipendente: str) -> Utente:
        '''
        Recupera il datore del dipendente

        Parametri
        ----------
        idDipendente : str
            Id del dipendente

        Returns
        -------
        AutenticazioneDAO.getDatore(idDipendente) : Utente
            Il Datore del Utente
        '''
        return AutenticazioneDAO.getDatore(idDipendente)
