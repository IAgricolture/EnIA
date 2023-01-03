import flask_pymongo
from flask_pymongo import PyMongo
from src import app

#Connessione al provider mondoDbAltas
print(app.config["MONGO_URI"])
mongo = PyMongo(app)

#Assegnazione alla variabile db il database enia
db = mongo.db.EnIA

#Documenti utente
utenti = db.Utente

#Documenti licenza
licenze = db.Licenza