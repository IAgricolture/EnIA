import datetime

#Scheletro della classe licenza così come è presente sul database
class Licenza():
    def __init__(self, id:str, tipo: str, costo: float, data_attivazione: str, data_scadenza:str, scaduta: bool, proprietario: str):
        
        self.id = id
        self.tipo = tipo
        self.costo = costo
        self.data_attivazione = data_attivazione
        self.data_scadenza = data_scadenza
        self.scaduta = scaduta
        self.proprietario = proprietario
    
    def __eq__(self, __o: object) -> bool:
        if(self.tipo == __o.tipo and self.costo == __o.costo and self.data_attivazione == __o.data_attivazione and self.data_scadenza == __o.data_scadenza and self.scaduta == __o.scaduta and self.proprietario == __o.proprietario):
            return True
        else:
            return False



