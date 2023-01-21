import uuid
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.model.Licenza import Licenza
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from src.logic.model.Utente import Utente


def random_string(length):
    return str(uuid.uuid4()).replace('-', '')[:length]

class GestioneUtenteService():
    
    def modificaUtente(current_user):
        return AutenticazioneDAO.modificaUtente(current_user)
        
    def modificaMetodo(mp: MetodoDiPagamento, num_carta:str, titolare:str, scadenza:str, cvv:str):
        mp.num_carta = num_carta
        mp.titolare = titolare
        mp.scadenza = scadenza
        mp.cvv = cvv
        return MetodoDiPagamentoDAO.modificaMetodo(mp)
     
    def findLicenzaByProprietario(id:str)->Licenza:
        return LicenzaDAO.findLicenzaByProprietario(id)    
    
    def getUtenti(id: str)-> list:
        return AutenticazioneDAO.listaDipendenti(id)

    def findMetodoByProprietario(id:str)->MetodoDiPagamento:
        return MetodoDiPagamentoDAO.findMetodoByProprietario(id)
    
    def GenerateCode(ruolo:str, datore:str) -> str:
        while True:
            codice = random_string(6)
            if(AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice) is None):
                break
        AutenticazioneDAO.insertSlot(ruolo, codice, datore)
        return codice
        

