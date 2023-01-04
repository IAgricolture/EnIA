import flask_pymongo
from flask_pymongo import PyMongo
from src import app

#Connessione al provider mondoDbAltas
mongo = PyMongo(app)

#Assegnazione alla variabile db il database enia
db = mongo.db.client.EnIA

#Documenti utente
utenti = db.Utente

#Documenti licenza
licenze = db.Licenza

#Documenti terreni
terreni = db.terreni

#Documenti metodo di pagamento
metodi_di_pagamento = db.Metodo_di_pagamento