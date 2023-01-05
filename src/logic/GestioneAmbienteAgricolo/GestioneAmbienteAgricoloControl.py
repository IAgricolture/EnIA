from flask import jsonify, request, render_template
from src import app
from flask import url_for
from src.logic.model.Terreno import Terreno
from src.logic.model.TerrenoDAO import TerrenoDAO

class AmbienteAgricoloControl():
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
            return jsonify({"terrenoJSON": terreno, "trovato": "true"})
