import datetime

#Scheletro della classe licenza così come è presente sul database
class Licenza():
    def __init__(self, id:str, tipo: str, costo: float, data_attivazione: datetime, data_scadenza:datetime, scaduta: bool):
        
        self.id = id
        self.tipo = tipo
        self.costo = costo
        self.data_attivazione = data_attivazione
        self.data_scadenza = data_scadenza
        self.scaduta = scaduta
    
    def __init__(self):
        pass



