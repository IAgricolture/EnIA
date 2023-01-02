import datetime
import hashlib

#Scheletro della classe utente così come è presente sul database
class Utente:
    def __init__(self, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: datetime, partitaIVA: str, codice: str, indirizzo: str):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        
        self.ruolo = ruolo
        self.dataNascita = dataNascita,
        self.partitaIVA = partitaIVA
        self.codice = codice
        self.indirizzo = indirizzo

        # Hash the password
        hash_object = hashlib.sha256(password.encode())
        # Get the hexadecimal representation of the hash
        hashed_password = hash_object.hexdigest()
        self.password = hashed_password
    
    def __init__(self):
        pass



