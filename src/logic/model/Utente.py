from datetime import datetime
import hashlib
import json

#Scheletro della classe utente così come è presente sul database
class Utente():
    def __init__(self, id:str, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: str, partitaIVA: str, codice: str, indirizzo: str):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.ruolo = ruolo
        self.indirizzo = indirizzo
        self.dataNascita = dataNascita
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



