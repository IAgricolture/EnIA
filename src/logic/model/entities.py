
import datetime

#Scheletro della classe utente così come è presente sul database
class Utente:
    def __init__(self, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: datetime, partitaIVA: str, codice: str, indirizzo: str):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
        self.ruolo = ruolo
        self.dataNascita = dataNascita,
        self.partitaIVA = partitaIVA
        self.codice = codice
        self.indirizzo = indirizzo


