from flask import jsonify, request, render_template, Response, make_response
from src import app
from flask import url_for
import json
from src.logic.model.Terreno import Terreno
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from flask_login import current_user

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
            proprietario = current_user.id
            
            risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, posizione, preferito, priorita, proprietario)
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
            risultato = AmbienteAgricoloService.modificaTerreno(idTerreno, nome, coltura, posizione, preferito, priorita, current_user.id)
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
        indirizzo = posizioneapi["address"]
        if("town" in indirizzo): #Pontecagnano, Salerno le porta come town
            comune = indirizzo["town"]
        else:
            comune = indirizzo["city"]  #Avellino, Potenza
        provincia = indirizzo["county"]
        regione = indirizzo["state"]
        nazione = indirizzo["country"]
        inquinamentoapi = AmbienteAgricoloService.cercaInquinamento(provincia, regione, nazione, comune)
        lat = AmbienteAgricoloService.cercalat(idTerreno)
        lon = AmbienteAgricoloService.cercalon(idTerreno)
        meteoapi = AmbienteAgricoloService.cercaMeteo(lat,lon)
        return render_template("dettagliterreno.html", terreno = terreno, posizioneapi = posizioneapi, inquinamentoapi = inquinamentoapi, meteoapi=meteoapi)
    
    @app.route("/getStoricoInquinamento", methods=["POST"])
    def getStoricoInquinamento():
        richiesta = request.get_json()
        idTerreno = richiesta.get("idTerreno")
        dataInizio = richiesta.get("dataInizio")
        dataFine = richiesta.get("dataFine")
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        #Ottengo dati dal display_name in quanto funziona per qualsiasi località (per altre non italiane, cambiano i nomi delle chiavi json)
        indirizzo = posizioneapi["address"]
        if("town" in indirizzo): #Pontecagnano, Salerno le porta come town
            comune = indirizzo["town"]
        else:
            comune = indirizzo["city"]  #Avellino, Potenza
        provincia = indirizzo["county"]
        regione = indirizzo["state"]
        nazione = indirizzo["country"]
        storicoinquinamentoapi = AmbienteAgricoloService.cercaStoricoInquinamento(dataInizio, dataFine, comune, regione, nazione, provincia, "json")
        return jsonify(storicoinquinamentoapi)
    
    @app.route("/downloadStoricoInquinamento", methods=["POST"])
    def downloadStoricoInquinamento():
        richiesta = request.get_json()
        idTerreno = richiesta.get("idTerreno")
        dataInizio = richiesta.get("dataInizio")
        dataFine = richiesta.get("dataFine")
        formato = richiesta.get("formato")
        print(formato)
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        #Ottengo dati dal display_name in quanto funziona per qualsiasi località (per altre non italiane, cambiano i nomi delle chiavi json)
        indirizzo = posizioneapi["address"]
        if("town" in indirizzo): #Pontecagnano, Salerno le porta come town
            comune = indirizzo["town"]
        else:
            comune = indirizzo["city"]  #Avellino, Potenza
        provincia = indirizzo["county"]
        regione = indirizzo["state"]
        nazione = indirizzo["country"]
        storicoinquinamentoapi = AmbienteAgricoloService.cercaStoricoInquinamento(dataInizio, dataFine, comune, regione, nazione, provincia, formato)
        if(formato == "json"):
            storicoinquinamentoapi = json.dumps(storicoinquinamentoapi) #Da testo, a stringa json formattata
        response = make_response(storicoinquinamentoapi)    #Lo rende una response http
        response.headers['Content-Disposition'] = "attachment; filename=storico." + str(formato) #Il filename è inutile, però va bene perchè rende consistenti client e server (?)
        response.mimetype = "text/" + str(formato)  #Dice il tipo di file
        print(response)
        print(response.headers)
        return response
    
    @app.route("/aggiungiIrrigatore", methods=["POST", "GET"])
    def aggiungiIrrigatore():
        if request.method == "POST":
            richiesta = request.get_json()
            idTerreno = richiesta.get("idTerreno")
            nomeIrrigatore = richiesta.get("nomeIrrigatore")
            posizioneIrrigatore = richiesta.get("posizioneIrrigatore")
            idTerreno = AmbienteAgricoloService.aggiungiIrrigatore(idTerreno, nomeIrrigatore, posizioneIrrigatore)
            return jsonify({"risposta": "true", "idIrrigatore": idTerreno})
    
    @app.route("/getIrrigatore", methods=["POST", "GET"])
    def getIrrigatore():
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            irrigatore = AmbienteAgricoloService.getIrrigatore(idIrrigatore)
            return jsonify({"idIrrigatore": irrigatore.id, "nomeIrrigatore": irrigatore.nome, "posizioneIrrigatore": irrigatore.posizione})
    
    @app.route("/modificaIrrigatore", methods=["POST", "GET"])
    def modificaIrrigatore():
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            nomeIrrigatore = richiesta.get("nomeIrrigatore")
            posizioneIrrigatore = richiesta.get("posizioneIrrigatore")
            AmbienteAgricoloService.modificaIrrigatore(idIrrigatore, nomeIrrigatore, posizioneIrrigatore)
            return jsonify({"risposta": "true"})
    
    @app.route("/visualizzaIrrigatori", methods=["POST", "GET"])
    def visualizzaIrrigatori():
        if request.method == "POST":
            richiesta = request.get_json()
            idTerreno = richiesta.get("idTerreno")
            irrigatori = AmbienteAgricoloService.visualizzaListaIrrigatori(idTerreno)
            return jsonify(irrigatori)

    @app.route("/eliminaIrrigatore", methods=["POST", "GET"])
    def eliminaIrrigatore():
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            AmbienteAgricoloService.eliminaIrrigatore(idIrrigatore)
            return jsonify({"risposta": "true"})
        
    @app.route("/attivaDisattivaIrrigatore", methods=["POST", "GET"])
    def attivaDisattivaIrrigatore():
        if request.method == "POST":
            richiesta = request.get_json()
            print(richiesta)
            idIrrigatore = richiesta.get("idIrrigatore")
            risposta = AmbienteAgricoloService.attivaDisattivaIrrigatore(idIrrigatore)
            if risposta:
                return jsonify({"risposta": "attivato"})
            else:
                return jsonify({"risposta": "disattivato"})
            
    @app.route("/visualizzaTerreni", methods=["POST", "GET"])
    def visualizzaTerreni():
        listaTerreni =  AmbienteAgricoloService.visualizzaTerreni(current_user.id)

        return render_template("visualizzaTerreni.html",listaTerreni = listaTerreni )
                
       
