
import hashlib
import re
from src.logic.model.Utente import Utente
from geopy.geocoders import Nominatim
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
    
    def creaUtente(nome:str, cognome:str, email:str, password:str, dataDiNascita:str, codice:str, indirizzo:str):
        slotUtente = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice)
        print(password)
        #decrypt password from sha512 to plain text
        
        risposta = {
            "nomeNonValido": False,
            "cognomeNonValido": False,
            "emailNonValida": False,
            "passwordNonValida": False,
            "indirizzoNonValido": False,
            "emailUsata": False,
            "codiceNonValido": False,
            "utenteRegistrato" : False,
            "nomeNonValido" : False,
            }

        nomereg = re.compile(r'^[a-z ]{2,30}$', re.IGNORECASE)
        mailreg = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}', re.IGNORECASE)
        #passreg = "/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$/"
        passreg = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@#$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$', re.IGNORECASE)
        #indireg = "/^[A-Za-zÀ-ù0-9 ,‘-]+$/"
        indireg = re.compile(r'^[A-Za-zÀ-ù0-9 ,‘-]+$', re.IGNORECASE)
        #controlla che il pattern del nome sia valido
        if not re.match(nomereg, nome):
            risposta["nomeNonValido"] = True
        if not re.match(nomereg, cognome):
            risposta["cognomeNonValido"] = True
        if not re.match(mailreg, email):
            risposta["emailNonValida"] = True
        if not re.match(passreg, password):
            risposta["passwordNonValida"] = True
        if not re.match(indireg, indirizzo):
            risposta["indirizzoNonValido"] = True
        #use nominatim to check if the address exists
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(indirizzo)
        if location == None:
            risposta["indirizzoNonValido"] = True
        #Se l'email è già usata il server avviserà il front-end
        if AutenticazioneDAO.trovaUtenteByEmail(email) != None:
            risposta["emailUsata"] = True
            #Se il codice è già usato oppure non è valido il server avviserà il front end
        if slotUtente is None or slotUtente.nome != "":
            risposta["codiceNonValido"] = True
            #Altrimenti si recupera lo slot Utente dal database lo si modifica con i dati utente
        print(risposta)
        if not risposta["nomeNonValido"] and not risposta["cognomeNonValido"] and not risposta["emailNonValida"] and not risposta["passwordNonValida"] and not risposta["indirizzoNonValido"] and not risposta["emailUsata"] and not risposta["codiceNonValido"]:
            slotUtente.nome = nome
            slotUtente.cognome = cognome
            slotUtente.password = hashlib.sha512(password.encode()).hexdigest()
            slotUtente.email = email
            slotUtente.dataNascita = dataDiNascita
            slotUtente.indirizzo = indirizzo
            print(slotUtente.nome)
            AutenticazioneDAO.modificaUtente(slotUtente)
            risposta["utenteRegistrato"] = True 
        
        return risposta

    def creaFarmer(nome:str, cognome:str, email:str, password:str, dataDiNascita:str, partitaiva:str, indirizzo:str)->str:  #Restituisce l'id
        utente = Utente("", nome, cognome, email, password, "farmer", dataDiNascita, partitaiva, None, indirizzo, None)
        return AutenticazioneDAO.creaUtente(utente)
    
    def creaLicenza(id:str, tipo:str)->Licenza:
        l = Licenza("", tipo, 5000, datetime.now().date().isoformat(), datetime.now().date().isoformat(), False, id)
        return LicenzaDAO.creaLicenza(l)
    
    
