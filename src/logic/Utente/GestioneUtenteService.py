import uuid
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.model.Licenza import Licenza
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from src.logic.model.Utente import Utente


def random_string(length):
    '''Genera un stringa randomica'''
    return str(uuid.uuid4()).replace('-', '')[:length]


class GestioneUtenteService():
    '''
    Classe Service di Gestione Utente

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    modificaUtente(current_user):
        Permette la modifica dei dati di un utente
    modificaMetodo(mp: MetodoDiPagamento, num_carta:str, titolare:str, scadenza:str, cvv:str):
        Permette la modifica dei dati di un metodo di pagamento
    findLicenzaByProprietario(id:str):
        Cerca la licenza di un utente farmer
    getUtenti(id: str):
        Permette di recuperare la lista dei dipendenti di un utente farmer
    findMetodoByProprietario(id:str):
        Cerca il metodo di un utente farmer
    removeUtenteFromAzienda(id:str):
        Rimuove un dipendente
    GenerateCode(ruolo:str, datore:str):
        Genera un codice di accesso per un dipendente
    '''

    def modificaUtente(current_user):
        '''
        Permette la modifica dei dati di un utente

        Parametri
        ----------
        current_user : Utente
            Utente da modificare

        Returns
        -------
        None
        '''
        return AutenticazioneDAO.modificaUtente(current_user)

    def modificaMetodo(mp: MetodoDiPagamento, num_carta: str,
                       titolare: str, scadenza: str, cvv: str):
        '''
        Permette la modifica dei dati di un metodo di pagamento

        Parametri
        ----------
        mp : MetodoDiPagamento
            Metodo Di Pagamento da modificare
        num_carta : str
            Numero della carta
        titolare : str
            Titolare della carta
        scadenza : str
            Scadenza della carta
        cvv : str
            Cvv della carta

        Returns
        -------
        None
        '''
        mp.num_carta = num_carta
        mp.titolare = titolare
        mp.scadenza = scadenza
        mp.cvv = cvv
        return MetodoDiPagamentoDAO.modificaMetodo(mp)

    def findLicenzaByProprietario(id: str) -> Licenza:
        '''
        Cerca la licenza di un utente farmer

        Parametri
        ----------
        id : str
            Id utente farmer

        Returns
        -------
        LicenzaDAO.findLicenzaByProprietario(id) : Licenza
            Licenza recuperata
        '''
        return LicenzaDAO.findLicenzaByProprietario(id)

    def getUtenti(id: str) -> list:
        '''
        Permette di recuperare la lista dei dipendenti di un utente farmer

        Parametri
        ----------
        id : str
            Id utente farmer

        Returns
        -------
        AutenticazioneDAO.listaDipendenti(id) : list
            Lista dei dipendenti
        '''
        return AutenticazioneDAO.listaDipendenti(id)

    def findMetodoByProprietario(id: str) -> MetodoDiPagamento:
        '''
        Cerca il metodo di un utente farmer

        Parametri
        ----------
        id : str
            Id utente farmer

        Returns
        -------
        MetodoDiPagamentoDAO.findMetodoByProprietario(id) : MetodoDiPagamento
            MetodoDiPagamento recuperato
        '''
        return MetodoDiPagamentoDAO.findMetodoByProprietario(id)

    def removeUtenteFromAzienda(id: str) -> bool:
        '''
        Rimuove un dipendente

        Parametri
        ----------
        id : str
            Id utente da rimuovere

        Returns
        -------
        None
        '''
        return AutenticazioneDAO.eliminaUtente(id)

    def GenerateCode(ruolo: str, datore: str) -> str:
        '''
        Genera un codice di accesso per un dipendente

        Parametri
        ----------
        ruolo : str
            Ruolo del dipendente
        datore : str
            Id utente farmer

        Returns
        -------
        codice : str
            Il codice di accesso
        "Error" : str
            Non è stato possibile generare il codice
        '''
        ruoli = ["irrigation manager", "pollution analyst"]

        if ruolo in ruoli:
            while True:
                codice = random_string(6)
                if (AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice) is None):
                    break
            AutenticazioneDAO.insertSlot(ruolo, codice, datore)
            return codice
        return "Error"
