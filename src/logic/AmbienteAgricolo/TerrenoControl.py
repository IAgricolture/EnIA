import hashlib
from src.logic.model.Terreno import Terreno

from src.logic.model.TerrenoDAO import TerrenoDAO


from flask import jsonify, request, render_template
from src import app
from flask_login import login_user
from flask import url_for

class TerrenoControl():
    @app.route("/aggiuntaterreno")
    def aggiungiTerreno():
        richiesta = request.args
        print(richiesta)
        nome = richiesta.get("nome")
        coltura = richiesta.get("coltura")
        posizione = richiesta.get("posizione")
        preferito = richiesta.get("preferito")
        priorita = richiesta.get("priorita")
        

        risposta = {
            "TerrenoAggiunto" : False
        }

        #MeMO: per salvarlo ne DB
        NewTerreno = Terreno(nome,coltura,posizione,preferito,priorita)
        TerrenoDAO.InserisciTerreno(NewTerreno)

        risposta["TerrenoAggiunto"] = True
        #TODO implememtare i controlli per l'aggiunta

        #Invio della risposta al server in formato json
        return jsonify(risposta)

        
        

        

        
        

