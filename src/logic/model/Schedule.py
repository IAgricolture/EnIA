import datetime

#Scheletro della classe Schedule così come è presente sul database
class Schedule():
    def __init__(self, id:str, inizio: datetime.time, fine: datetime.time, modalita: str):
        
        self.id = id
        self.inizio = inizio
        self.fine = fine
        self.modalita = modalita


