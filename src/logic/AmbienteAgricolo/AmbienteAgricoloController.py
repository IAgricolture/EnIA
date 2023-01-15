from flask import jsonify, request, render_template
from src import app
from flask import url_for
import json
from src.logic.model.Terreno import Terreno
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService

class AmbienteAgricoloController():

    @app.route("/aggiuntaTerreno", methods=["POST", "GET"])
    def aggiungiTerreno():
        if(request.method != "POST"):
            return render_template("aggiuntaterreno.html")
        elif request.method == "POST":
            
            richiesta = request.get_json()
            nome = richiesta.get("nome")
            coltura = richiesta.get("coltura")
            posizione = richiesta.get("posizione")
            preferito = richiesta.get("preferito")
            priorita = richiesta.get("priorita")
            
            risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, posizione, preferito, priorita)
            risposta = {
                "TerrenoAggiunto" : "True" #TODO:QUI CI VA IL RISULTATO
            }
            #TODO implememtare i controlli per l'aggiunta

            #Invio della risposta al server in formato json
            return jsonify(risposta)


    @app.route("/modificaTerreno", methods=["POST", "GET"])
    def cercaModificata():
        if request.method != "POST":
            idTerreno = request.args.get("idTerreno")
            terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
            print(terreno)
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
            risultato = AmbienteAgricoloService.modificaTerreno(idTerreno, nome, coltura, posizione, preferito, priorita)
            return jsonify({"modificato": "true"})



    @app.route("/eliminaTerreno", methods = ["POST", "GET"])
    def elimina():
        """ 
        #TODO Scrivere documenzione
        """
        if(request.method != "POST"):
            idTerreno = request.args.get("idTerreno")
            terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
            return render_template("eliminaterreno.html", terreno = terreno)
        elif request.method == "POST":
            richiesta = request.get_json()
            print(str(richiesta))
            idTerreno = str(richiesta)   
            risultato = AmbienteAgricoloService.eliminaTerreno(idTerreno)
            #TODO:MIGLIORARE CON BOOLEANI
            if(risultato):
                return jsonify({"trovato" : "true"})
            else:
                return jsonify({"trovato" : "false"})
        
    @app.route("/dettagliterreno", methods = ["POST", "GET"])
    def dettagli():
        idTerreno = request.args.get("idTerreno")
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        #Ottengo dati dal display_name in quanto funziona per qualsiasi località (per altre non italiane, cambiano i nomi delle chiavi json)
        posizione = posizioneapi["display_name"].split(", ") #Ottengo in una lista i dati
        print(posizione)
        citta = posizione[0]    #Inutilizzata per adesso, lasciata qui se dovesse servire
        comune = posizione[1]
        regione = posizione[2]
        if(len(posizione) == 4):   #Parse per evitare il codice postale, soluzione temporanea.
            nazione = posizione[3]
        else:
            nazione = posizione[4]
        inquinamentoapi = AmbienteAgricoloService.cercaInquinamento(comune, regione, nazione)
        storicoinquinamentoapi = AmbienteAgricoloService.cercaStoricoInquinamento("2022-09-01", "2022-09-30", citta, regione, nazione, comune)
        return render_template("dettagliterreno.html", terreno = terreno, posizioneapi = posizioneapi, inquinamentoapi = inquinamentoapi, storicoinquinamentoapi = storicoinquinamentoapi)