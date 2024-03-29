from datetime import datetime
import hashlib
import json

# Scheletro della classe utente così come è presente sul database


class Utente():
    def __init__(self, id: str, nome: str, cognome: str, email: str, password: str, ruolo: str,
                 dataNascita: str, partitaIVA: str, codice: str, indirizzo: str, datore: str):
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

    # Se esiste, allora è autenticato, perciò true. Serve per @login_required.
    def is_authenticated(self):
        return True

    def is_active(self):  # Controlla che l'utente non sia stato cancellato (Potrebbe essere utile per rimuovere ruoli, o cancellazione terreno.)
        return True

    # Se esiste, di sicuro non può essere anonimo, perciò false. Serve per
    # @login_required.
    def is_anonymous(self):
        return False

    def __eq__(self, __o: object) -> bool:
        if(self.nome == __o.nome and self.cognome == __o.cognome and self.email == __o.email and self.ruolo == __o.ruolo and self.indirizzo == __o.indirizzo and self.dataNascita == __o.dataNascita and self.partitaIVA == __o.partitaIVA and self.codice == __o.codice and self.datore == __o.datore and self.password == __o.password):
           return True 
        else:
            return False
        


