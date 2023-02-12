

# Scheletro della classe Impianto Di Irrigazione così come è presente sul
# database
class ImpiantoDiIrrigazione():
    def __init__(self, id: str, nome: str, tipo: str,
                 codice: str, posizione: str, attivo: bool):

        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.codice = codice
        self.attivo = attivo
        self.posizione = posizione
        
    def __eq__(self, __o: object) -> bool:
        if(self.nome == __o.nome and self.tipo == __o.tipo and self.codice == __o.codice and self.attivo == __o.attivo and self.posizione == __o.posizione):
            return True
        else:
            return False


