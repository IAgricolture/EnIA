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


    @app.route("/modificaTerreno", methods=["POST", "GET"])
    def cercaModificata():
        if request.method != "POST":
            idTerreno = request.args.get("idTerreno")
            terreno = TerrenoDAO.TrovaTerreno(idTerreno)
            return render_template("modifyterrain.html", terreno = terreno, posizione = terreno.posizione)
        elif request.method == "POST":
            richiesta = request.get_json()
            print(str(richiesta))
            idTerreno = richiesta.get("idTerreno")
            nome = richiesta.get("nome")
            coltura = richiesta.get("coltura")
            posizione = richiesta.get("posizione")
            preferito = richiesta.get("preferito")
            priorita = richiesta.get("priorita")
            terreno = Terreno(idTerreno, nome, coltura, posizione, preferito, priorita)
            print(terreno)
            TerrenoDAO.modificaTerreno(terreno)
            return jsonify({"modificato": "true"})



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