

# Scheletro della classe Metodo di pagamento così come è presente sul database
class MetodoDiPagamento():
    def __init__(self, id: str, num_carta: str, titolare: str,
                 scadenza: str, cvv: str, proprietario: str):

        self.id = id
        self.num_carta = num_carta
        self.titolare = titolare
        self.scadenza = scadenza
        self.cvv = cvv
        self.proprietario = proprietario
