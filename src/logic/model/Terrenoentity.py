from bson.objectid import ObjectId
from typing import List
class Terreno():
    def __init__(self, id:str, nome: str, coltura: str, posizione: str, preferito: bool, priorita:int, listautenti: str):

        self.id = id
        self.nome = nome
        self.coltura = coltura
        self.posizione = posizione
        self.preferito = preferito
        self.priorita = priorita
        self.listautenti = listautenti

    def getid(self):
        return str(self.id)

    def getnome(self):
        return str(self.nome)

    def getcoltura(self):
        return str(self.coltura)

    def getposizione(self):
        return str(self.posizione)

    def getlistautenti(self):
        return str(self.listautenti)

    def getpreferito(self):
        return bool(self.preferito)
        
    def getpriorita(self):
        return int(self.priorita)

    def __init__(self):
        pass