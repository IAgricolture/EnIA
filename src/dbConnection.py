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
terreni = db.Terreno

#Documenti metodo di pagamento
metodi_di_pagamento = db.Metodo_di_pagamento

#Documenti evento
eventi = db.Evento

#Documenti schedule
schedule = db.Schedule

#Documenti impianto di irrigazione
impianti = db.Impianto_di_irrigazione

#Documenti dati meteo
datimeteo = db.Dati_Meteo

#Documenti dati inquinamento
datiinqui = db.Dati_Inquinamento