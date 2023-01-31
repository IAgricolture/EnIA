

#Scheletro della classe Metodo di pagamento così come è presente sul database
class MetodoDiPagamento():
    def __init__(self, id:str, num_carta: str, titolare: str, scadenza: str, cvv:str, proprietario: str):
        
        self.id = id
        self.num_carta = num_carta
        self.titolare = titolare
        self.scadenza = scadenza
        self.cvv = cvv
        self.proprietario = proprietario
        
    def __eq__(self, __o: object) -> bool:
        if(self.num_carta == __o.num_carta and self.titolare == __o.titolare and self.scadenza == __o.scadenza and self.cvv == __o.cvv and self.proprietario == __o.proprietario):
            return True
        else:
            return False
    
