from datetime import datetime

#Scheletro della classe Schedule così come è presente sul database
class Schedule():
    
    modalita = ["nessuno", "basso", "medio", "alto"]
    
    def __init__(self, id:str, inizio: datetime.time, fine: datetime, modalita: str, terreno: str):
        
        self.id = id
        self.inizio = inizio
        self.fine = fine
        self.modalita = modalita
        self.terreno = terreno


