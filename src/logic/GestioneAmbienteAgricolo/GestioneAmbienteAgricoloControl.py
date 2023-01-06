from flask import jsonify, request, render_template
from src import app
from flask import url_for
import json
from src.logic.model.Terreno import Terreno
from src.logic.model.TerrenoDAO import TerrenoDAO

class AmbienteAgricoloControl():

    @app.route("/aggiuntaterreno", methods=["POST"])
    def aggiungiTerreno():
        richiesta = request.get_json()
        id = None
        nome = richiesta.get("nome")
        coltura = richiesta.get("coltura")
        posizione = richiesta.get("posizione")
        preferito = richiesta.get("preferito")
        priorita = richiesta.get("priorita")

        risposta = {
            "TerrenoAggiunto" : False
        }

        #MeMO: per salvarlo ne DB
        NewTerreno = Terreno(id,nome,coltura,posizione,preferito,priorita)
        TerrenoDAO.InserisciTerreno(NewTerreno)

        risposta["TerrenoAggiunto"] = True
        #TODO implememtare i controlli per l'aggiunta

        #Invio della risposta al server in formato json
        return jsonify(risposta)


    @app.route("/modifyterrain", methods = ["GET"])
    def cerca():
        """ Chiama il metodo TrovaTerreno da TerrenoDAO, se lo trova lo restituisce, assieme ad un messaggio di successo,
            altrimenti restituisce None ed un messaggio di errore.
        """
        idTerreno : str = request.args.get("idTerreno") #Se non str, sicuramente fallisce, trovaTerreno si aspetta str
        print("idTerreno inserito: " + idTerreno)
        if len(idTerreno) != 24:    #Controllo che sia un id MongoDB valido
            print("Errore: Id inserito non valido.")
            return jsonify({"terrenoJSON": None, "trovato" : "false"})
        terreno = TerrenoDAO.TrovaTerreno(idTerreno)
        if terreno is None: #Non l'ha trovato
            return jsonify({"terrenoJSON": None, "trovato" : "false"})
        else:  
            json1 = json.dumps(terreno.__dict__)
            return jsonify({"terrenoJSON": json1, "trovato": "true"})


    @app.route("/eliminaTerreno", methods = ["GET"])
    def elimina():
        """ 
        #TODO Scrivere documenzione
        """
        idTerreno : str = request.args.get("idTerreno") #Se non str, sicuramente fallisce, trovaTerreno si aspetta str
        print("idTerreno inserito: " + idTerreno)
        if len(idTerreno) != 24:    #Controllo che sia un id MongoDB valido
            print("Errore: Id inserito non valido.")
            
        terreno = TerrenoDAO.TrovaTerreno(idTerreno)
        if terreno is None: #Non l'ha trovato
            print("Nessun Terreno trovato con questo id")
            return jsonify({"trovato" : "false"})
        else:  
            TerrenoDAO.RimuoviTerreno(terreno)
            print("Terreno Eliminato ")
            return jsonify({ "trovato": "true"})