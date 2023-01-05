import datetime
import hashlib

#Scheletro della classe utente così come è presente sul database
class Utente():
    def __init__(self, id:str, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: datetime, partitaIVA: str, codice: str, indirizzo: str):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.ruolo = ruolo
        self.dataNascita = dataNascita,
        self.indirizzo = indirizzo
        if ruolo == "farmer":
            self.partitaIVA = partitaIVA
            self.codice = None
        else: 
            self.codice = codice
            self.partitaIVA = None
    

        self.password = password

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")



