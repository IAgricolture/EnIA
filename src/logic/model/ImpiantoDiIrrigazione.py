

#Scheletro della classe Impianto Di Irrigazione così come è presente sul database
class ImpiantoDiIrrigazione():
    def __init__(self, id:str, nome: str, tipo: str, codice: str, attivo:bool):
        
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.codice = codice
        self.attivo = attivo
    
    def __init__(self):
        pass



