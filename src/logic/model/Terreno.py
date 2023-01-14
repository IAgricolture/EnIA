from bson.objectid import ObjectId
from typing import List
class Terreno():
    def __init__(self, id:str, nome: str, coltura: str, posizione, preferito: bool, priorita:int, proprietario: str):

        self.id = id
        self.nome = nome
        self.coltura = coltura
        self.posizione = posizione
        self.preferito = preferito
        self.priorita = priorita
        self.proprietario = proprietario  #Quando avremo l'utente andremo ad implementarlo bene

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

    