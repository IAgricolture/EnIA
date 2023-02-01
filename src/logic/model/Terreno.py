from bson.objectid import ObjectId
from typing import List


class Terreno():
    def __init__(self, id: str, nome: str, coltura: str, stadio_crescita,
                 posizione, preferito: bool, priorita: int, proprietario: str):

        self.id = id
        self.nome = nome
        self.coltura = coltura
        self.stadio_crescita = stadio_crescita
        self.posizione = posizione
        self.preferito = preferito
        self.priorita = priorita
        self.proprietario = proprietario

    def getid(self):
        return str(self.id)

    def getnome(self):
        return str(self.nome)

    def getcoltura(self):
        return str(self.coltura)

    def getposizione(self):
        return str(self.posizione)

    def getpreferito(self):
        return bool(self.preferito)

    def getpriorita(self):
        return int(self.priorita)

    def getproprietario(self):
        return str(self.proprietario)

    # Fa da equals, lo metto senza il controllo dell'id in quanto con l'id non
    # mi serve, invece così lo uso per test e per duplicati.
    def __eq__(self, __o: object) -> bool:
        if (self.nome == __o.nome and self.coltura == __o.coltura and self.posizione == __o.posizione and self.preferito ==
                __o.preferito and self.priorita == __o.priorita and self.proprietario == __o.proprietario):
            return True
        else:
            return False
