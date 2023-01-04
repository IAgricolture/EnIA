import datetime

#Scheletro della classe Evento così come è presente sul database
class Evento():
    def __init__(self, id:str, titolo: str, descrizione: str, orario: datetime, tipo:str, azione_umana:bool, visto:bool):
        
        self.id = id
        self.titolo = titolo
        self.descrizione = descrizione
        self.orario = orario
        self.tipo = tipo
        self.azione_umana = azione_umana
        self.visto = visto
    
    def __init__(self):
        pass



