
from src.logic.model.Utente import Utente

from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.model.Licenza import Licenza
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from datetime import datetime
class RegistrazioneService():
    def trovaUtenteByCodiceDiAccesso(codice:str)->Utente:
        return AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice)
    
    def trovaUtenteByEmail(email:str)->Utente:
        return AutenticazioneDAO.trovaUtenteByEmail(email)
    
    def modificaUtente(nome:str, cognome:str, email:str, password:str, dataDiNascita:str, codice:str, indirizzo:str):
        slotUtente = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice)

        risposta = {
            "emailUsata": False,
            "codiceNonValido": False,
            "utenteRegistrato" : False
            }

        #Se l'email è già usata il server avviserà il front-end
        if AutenticazioneDAO.trovaUtenteByEmail(email) != None:
            risposta["emailUsata"] = True
            #Se il codice è già usato oppure non è valido il server avviserà il front end
        elif slotUtente == None or slotUtente.nome == None:
            risposta["codiceNonValido"] = True
            #Altrimenti si recupera lo slot Utente dal database lo si modifica con i dati utente
        else:
            slotUtente.nome = nome
            slotUtente.cognome = cognome
            slotUtente.password = password
            slotUtente.email = email
            slotUtente.dataNascita = dataDiNascita
            slotUtente.indirizzo = indirizzo
            AutenticazioneDAO.modificaUtente(slotUtente)
            risposta["utenteRegistrato"] = True 
        
        return risposta
    
    def creaFarmer(nome:str, cognome:str, email:str, password:str, dataDiNascita:str, partitaiva:str, indirizzo:str)->str:  #Restituisce l'id
        utente = Utente("", nome, cognome, email, password, "farmer", dataDiNascita, partitaiva, None, indirizzo, None)
        return AutenticazioneDAO.creaUtente(utente)
    
    def creaLicenza(id:str, tipo:str)->Licenza:
        l = Licenza("", tipo, 5000, datetime.now().date().isoformat(), datetime.now().date().isoformat(), False, id)
        return LicenzaDAO.creaLicenza(l)
    
    def creaMetodoDiPagamento(numerocarta, titolare, scadenza, cvv, id)->MetodoDiPagamento:
        m = MetodoDiPagamento("", numerocarta, titolare, scadenza, cvv, id)
        return MetodoDiPagamentoDAO.creaMetodo(m)