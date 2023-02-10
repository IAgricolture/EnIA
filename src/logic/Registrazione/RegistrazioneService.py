
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
    '''
    Classe Service di Ambiente Agricolo

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    trovaUtenteByCodiceDiAccesso(codice: str):
        Cerca un utente attraverso il suo codice di accesso
    trovaUtenteByEmail(email: str):
        Cerca un utente attraverso la sua email
    modificaUtente(nome: str, cognome: str, email: str, password: str, dataDiNascita: str, codice: str, indirizzo: str):
        Modifica i dati relativi ad un utente
    creaFarmer(nome: str, cognome: str, email: str, password: str, dataDiNascita: str, partitaiva: str, indirizzo: str):
        Crea un nuovo utente farmer
    creaLicenza(id: str, tipo: str):
        Crea una nuova licenza
    creaMetodoDiPagamento(numerocarta, titolare, scadenza, cvv, id):
        Crea una nuovo metodo di pagamento
    '''
    def trovaUtenteByCodiceDiAccesso(codice: str) -> Utente:
        '''
        Cerca un utente attraverso il suo codice di accesso

        Parametri
        ----------
        codice : str
            Codice di accesso

        Returns
        -------
        AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice) : Utente
            Utente a cui fa riferimento il codice di accesso
        '''
        return AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice)

    def trovaUtenteByEmail(email: str) -> Utente:
        '''
        Cerca un utente attraverso la sua email

        Parametri
        ----------
        email : str
            email

        Returns
        -------
        AutenticazioneDAO.trovaUtenteByEmail(email) : Utente
            Utente a cui fa riferimento la mail

        '''
        return AutenticazioneDAO.trovaUtenteByEmail(email)

    def creaUtente(nome: str, cognome: str, email: str, password: str,
                       dataDiNascita: str, codice: str, indirizzo: str):
        '''
        Modifica i dati relativi ad un utente

        Parametri
        ----------
        nome : str
            nome
        cognome : str
            cognome
        email : str
            email
        password : str
            password
        dataDiNascita : str
            Data di nascita
        codice : str
            codice di accesso
        indirizzo : str
            Indirizzo

        Returns
        -------
        risposta : dict
            Esito dell'operazione
        '''
        slotUtente = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice)
        print(password)
        # decrypt password from sha512 to plain text

        risposta = {
            "nomeNonValido": False,
            "cognomeNonValido": False,
            "emailNonValida": False,
            "passwordNonValida": False,
            "indirizzoNonValido": False,
            "emailUsata": False,
            "codiceNonValido": False,
            "utenteRegistrato": False,
            "nomeNonValido": False,
        }

        nomereg = re.compile(r'^[a-z ]{2,30}$', re.IGNORECASE)
        mailreg = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}', re.IGNORECASE)
        #passreg = "/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$/"
        passreg = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@#$!%*?&_])[A-Za-z\d$@$!%*?&_]{8,20}$', re.IGNORECASE)
        #indireg = "/^[A-Za-zÀ-ù0-9 ,‘-]+$/"
        indireg = re.compile(r'^[A-Za-zÀ-ù0-9 ,‘-]+$', re.IGNORECASE)
        # controlla che il pattern del nome sia valido
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
        # use nominatim to check if the address exists
        if risposta["indirizzoNonValido"] == False:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(indirizzo)
            if location is None:
                risposta["indirizzoNonValido"] = True
        # Se l'email è già usata il server avviserà il front-end
        if AutenticazioneDAO.trovaUtenteByEmail(email) is not None:
            risposta["emailUsata"] = True
            # Se il codice è già usato oppure non è valido il server avviserà
            # il front end
        if slotUtente is None or slotUtente.nome != "":

            risposta["codiceNonValido"] = True
            # Altrimenti si recupera lo slot Utente dal database lo si modifica
            # con i dati utente
        print(risposta)
        if not risposta["nomeNonValido"] and not risposta["cognomeNonValido"] and not risposta["emailNonValida"] and not risposta[
                "passwordNonValida"] and not risposta["indirizzoNonValido"] and not risposta["emailUsata"] and not risposta["codiceNonValido"]:
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

    def creaFarmer(nome: str, cognome: str, email: str, password: str, dataDiNascita: str, partitaiva: str, indirizzo: str) -> str:  # Restituisce l'id
        '''
        Crea un nuovo utente farmer

        Parametri
        ----------
        nome : str
            nome
        cognome : str
            cognome
        email : str
            email
        password : str
            password
        dataDiNascita : str
            Data di nascita
        partitaiva : str
            Partita IVA
        indirizzo : str
            Indirizzo

        Returns
        -------
        AutenticazioneDAO.creaUtente(utente) : str
            L'id del nuovo utente creato
        '''
        utente = Utente("", nome, cognome, email, password, "farmer",
                        dataDiNascita, partitaiva, None, indirizzo, None)

        return AutenticazioneDAO.creaUtente(utente)

    def creaLicenza(id: str, tipo: str) -> Licenza:
        '''
        Crea una nuova licenza

        Parametri
        ----------
        id : str
            Id del proprietario della licenza
        tipo : str
            tipo di licenza

        Returns
        -------
        LicenzaDAO.creaLicenza(l) : Licenza
            La licenza appena creata
        '''
        l = Licenza("", tipo, 5000, datetime.now().date().isoformat(),
                    datetime.now().date().isoformat(), False, id)
        return LicenzaDAO.creaLicenza(l)

    def creaMetodoDiPagamento(numerocarta, titolare,
                              scadenza, cvv, id) -> MetodoDiPagamento:
        '''
        Crea una nuovo metodo di pagamento

        Parametri
        ----------
        numerocarta : str
            Numero della carta
        titolare : str
            Titolare della carta
        scadenza : str
            Scadenza della carta
        cvv : str
            CVV della carta
        id : str
            Id dell'utilizzatore del metodo di pagamento

        Returns
        -------
        MetodoDiPagamentoDAO.creaMetodo(m) : MetodoDiPagamento
            Il metodo di pagamento appena creato
        '''
        m = MetodoDiPagamento("", numerocarta, titolare, scadenza, cvv, id)
        return MetodoDiPagamentoDAO.creaMetodo(m)
