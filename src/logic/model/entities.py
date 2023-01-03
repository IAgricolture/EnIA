import datetime
import hashlib

#Scheletro della classe utente così come è presente sul database
class Utente():
    def __init__(self,id:str, nome: str, cognome: str, email: str, password:str, ruolo: str, dataNascita: datetime, partitaIVA: str, codice: str, indirizzo: str):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        
        self.ruolo = ruolo
        self.dataNascita = dataNascita,
        self.partitaIVA = partitaIVA
        self.codice = codice
        self.indirizzo = indirizzo

        # Hash the password
        hash_object = hashlib.sha512(password.encode())
        # Get the hexadecimal representation of the hash
        hashed_password = hash_object.hexdigest()
        self.password = hashed_password

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")
    
    def __init__(self):
        pass



