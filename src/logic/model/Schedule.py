from datetime import datetime

# Scheletro della classe Schedule così come è presente sul database


class Schedule():

    modalita = ["nessuno", "basso", "medio", "alto"]

    def __init__(self, id: str, inizio: datetime.time,
                 fine: datetime, modalita: str, terreno: str):

        self.id = id
        self.inizio = inizio
        self.fine = fine
        self.modalita = modalita
        self.terreno = terreno
    
    def __eq__(self, __o: object) -> bool:
        try:
            if(self.inizio == __o.inizio and self.fine == __o.fine and self.modalita == __o.modalita and self.terreno == __o.terreno):
                return True
            else:
                return False
        except Exception as e:
            print(e)

