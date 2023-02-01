from datetime import datetime

#Scheletro della classe Evento così come è presente sul database
class Evento():
    def __init__(self, id:str, titolo: str, descrizione: str, orario: datetime, tipo:str, azione_umana:bool, visto:bool, terreno: str):
        
        self.id = id
        self.titolo = titolo
        self.descrizione = descrizione
        self.orario = orario
        self.tipo = tipo
        self.azione_umana = azione_umana
        self.visto = visto
        self.terreno = terreno
    
    def __eq__(self, __o: object) -> bool:
        if(self.titolo == __o.titolo and self.descrizione == __o.descrizione and self.orario == __o.orario and self.tipo == __o.tipo and self.azione_umana == __o.azione_umana and self.visto == __o.visto and self.terreno == __o.terreno):
            return True
        else:
            return False


