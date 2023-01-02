import pymongo
from pymongo import MongoClient

#Connessione al provider mondoDbAltas
client = MongoClient("mongodb+srv://enia:vp7CMyN7V5Rl8FZR@cluster0.o0m35vt.mongodb.net/?retryWrites=true&w=majority")

#Assegnazione alla variabile db il database enia
db = client.EnIA

#Documenti utente
utenti = db.users

