from datetime import datetime
import hashlib
import json

#Scheletro della classe utente così come è presente sul database
class Utente():
    def __init__(self, id:str, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: str, partitaIVA: str, codice: str, indirizzo: str, datore: str):
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
            self.datore = None
        else: 
            self.datore = datore
            self.codice = codice
            self.partitaIVA = None
    

        self.password = password

    

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")
    
    def is_authenticated(self): #Se esiste, allora è autenticato, perciò true. Serve per @login_required.
        return True

    def is_active(self):  #Controlla che l'utente non sia stato cancellato (Potrebbe essere utile per rimuovere ruoli, o cancellazione terreno.)
        return True

    def is_anonymous(self): #Se esiste, di sicuro non può essere anonimo, perciò false. Serve per @login_required.
        return False



