from flask import jsonify, request, render_template, Response, make_response, url_for, redirect
from src import app, farmer_required
import json
from src.logic.Autenticazione import AutenticazioneService
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.model.Terreno import Terreno
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from flask_login import current_user, login_required


class AmbienteAgricoloController():
    '''
    Classe Controller di Ambiente Agricolo

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    aggiungiTerreno():
        Permette l'aggiunta di un nuovo terreno all'utente farmer
    cercaModificata():
        Permette la modifica dei dati di un terreno all'utente farmer
    elimina():
        Permette l'eliminazione di un terreno all'utente farmer
    dettagli():
        Permette la visualizzazione di un terreno specifico
    getStoricoInquinamento():
        Permette la visualizzazione dello storico degli agenti inquinanti di un terreno
    downloadStoricoInquinamento():
        Permette il download dello storico inquinamento
    downloadStoricoInquinamento():
        Permette il download dello storico inquinamento
    aggiungiIrrigatore():
        Permette l'aggiunta di un irrigatore ad un utente
    getIrrigatore():
        Permette la visualizzazione di tutti gli irrigatori presenti su un terreno
    modificaIrrigatore():
        Permette la modifica dei dati di un irrigatore
    visualizzaIrrigatori():
        Permette la visualizzazionde di tutti gli irrigatori di un terreno
    eliminaIrrigatore():
        Permette l'eliminazione di un irrigatore
    attivaDisattivaIrrigatore():
        Permette l'attivazione e la disattivazione di un irrigatore
    visualizzaTerreni():
        Permette la visualizzazione di tutti i terreni di proprietà di utente farmer
    visualizzaPredizioneIrrigazione():
        Permette la visualizzazione della predizione di irrigazione fornita dal modulo AI
    '''
    @app.route("/aggiuntaTerreno", methods=["POST", "GET"])
    @login_required
    @farmer_required
    def aggiungiTerreno():
        '''Permette l'aggiunta di un nuovo terreno all'utente farmer'''
        if (request.method != "POST"):
            return render_template("aggiuntaterreno.html", colture=AmbienteAgricoloService.Colture,
                                   stadi_crescita=AmbienteAgricoloService.StadiCrescita)
        elif request.method == "POST":

            richiesta = request.get_json()
            nome = richiesta.get("nome")
            coltura = richiesta.get("coltura")
            posizione = richiesta.get("posizione")
            preferito = richiesta.get("preferito")
            priorita = richiesta.get("priorita")
            stadio_crescita = richiesta.get("stadio_crescita")
            proprietario = current_user.id

            risultato = AmbienteAgricoloService.aggiungiTerreno(
                nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
            risposta = {
                # TODO:QUI CI VA IL RISULTATO
                "TerrenoAggiunto": risultato["esitoOperazione"]
            }
            # TODO implememtare i controlli per l'aggiunta

            # Invio della risposta al server in formato json
            return jsonify(risposta)

    @app.route("/modificaTerreno", methods=["POST", "GET"])
    @farmer_required
    def cercaModificata():
        '''Permette la modifica dei dati di un terreno all'utente farmer'''
        if request.method != "POST":
            idTerreno = request.args.get("idTerreno")
            terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
            print(terreno.stadio_crescita)
            return render_template("modifyterrain.html", terreno=terreno, posizione=terreno.posizione,
                                   colture=AmbienteAgricoloService.Colture, stadi_crescita=AmbienteAgricoloService.StadiCrescita)
        elif request.method == "POST":
            richiesta = request.get_json()
            print(str(richiesta))
            idTerreno = richiesta.get("idTerreno")
            nome = richiesta.get("nome")
            coltura = richiesta.get("coltura")
            posizione = richiesta.get("posizione")
            preferito = richiesta.get("preferito")
            priorita = richiesta.get("priorita")
            stadio_crescita = richiesta.get("stadio_crescita")
            risultato = AmbienteAgricoloService.modificaTerreno(
                idTerreno, nome, coltura, stadio_crescita, posizione, preferito, priorita, current_user.id)
            return jsonify({"modificato": "true"})

    @app.route("/eliminaTerreno", methods=["GET"])
    @farmer_required
    def elimina():
        '''Permette l'eliminazione di un terreno all'utente farmer'''
        idTerreno = request.args.get("idTerreno")
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        risultato = AmbienteAgricoloService.eliminaTerreno(idTerreno)
        return redirect("/visualizzaTerreni")

    @app.route("/dettagliterreno", methods=["POST", "GET"])
    @login_required
    def dettagli():
        '''Permette la visualizzazione di un terreno specifico'''
        idTerreno = request.args.get("idTerreno")
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        try:
            indirizzo = posizioneapi["address"]
            if ("town" in indirizzo):  # Pontecagnano, Salerno le porta come town
                comune = indirizzo["town"]
            else:
                if ("city" in indirizzo):
                    comune = indirizzo["city"]  # Avellino, Potenza
                else:
                    comune = indirizzo["village"]  # Molise
            provincia = indirizzo["county"]
            regione = indirizzo["state"]
            nazione = indirizzo["country"]
            inquinamentoapi = AmbienteAgricoloService.cercaInquinamento(
                provincia, regione, nazione, comune)
        except KeyError:
            # Formato della posizione non si trova con quello standard, quindi
            # l'inquinamentoapi fallirà. Per evitare crash, gestisco qui
            # l'eccezione.
            inquinamentoapi = {
                'message': 'Impossibile soddisfare questa richiesta'
            }
        lat = AmbienteAgricoloService.cercalat(idTerreno)
        lon = AmbienteAgricoloService.cercalon(idTerreno)
        meteoapi = DecisionIntelligenceService.cercaMeteo(lat,lon)
        return render_template("dettagliterreno.html", terreno = terreno, posizioneapi = posizioneapi, inquinamentoapi = inquinamentoapi, meteoapi=meteoapi)
    
    @app.route("/getStoricoInquinamento", methods=["POST"])
    def getStoricoInquinamento():
        '''Permette la visualizzazione dello storico degli agenti inquinanti di un terreno'''
        richiesta = request.get_json()
        idTerreno = richiesta.get("idTerreno")
        dataInizio = richiesta.get("dataInizio")
        dataFine = richiesta.get("dataFine")
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        # Ottengo dati dal display_name in quanto funziona per qualsiasi
        # località (per altre non italiane, cambiano i nomi delle chiavi json)
        indirizzo = posizioneapi["address"]
        if ("town" in indirizzo):  # Pontecagnano, Salerno le porta come town
            comune = indirizzo["town"]
        else:
            comune = indirizzo["city"]  # Avellino, Potenza
        provincia = indirizzo["county"]
        regione = indirizzo["state"]
        nazione = indirizzo["country"]
        storicoinquinamentoapi = AmbienteAgricoloService.cercaStoricoInquinamento(
            dataInizio, dataFine, comune, regione, nazione, provincia, "json")
        return jsonify(storicoinquinamentoapi)

    @app.route("/downloadStoricoInquinamento", methods=["POST"])
    def downloadStoricoInquinamento():
        '''Permette il download dello storico inquinamento'''
        richiesta = request.get_json()
        idTerreno = richiesta.get("idTerreno")
        dataInizio = richiesta.get("dataInizio")
        dataFine = richiesta.get("dataFine")
        formato = richiesta.get("formato")
        print(formato)
        terreno = AmbienteAgricoloService.trovaTerreno(idTerreno)
        posizioneapi = AmbienteAgricoloService.cercaPosizione(idTerreno)
        print(posizioneapi)
        # Ottengo dati dal display_name in quanto funziona per qualsiasi
        # località (per altre non italiane, cambiano i nomi delle chiavi json)
        indirizzo = posizioneapi["address"]
        if ("town" in indirizzo):  # Pontecagnano, Salerno le porta come town
            comune = indirizzo["town"]
        else:
            comune = indirizzo["city"]  # Avellino, Potenza
        provincia = indirizzo["county"]
        regione = indirizzo["state"]
        nazione = indirizzo["country"]
        storicoinquinamentoapi = AmbienteAgricoloService.cercaStoricoInquinamento(
            dataInizio, dataFine, comune, regione, nazione, provincia, formato)
        if (formato == "json"):
            # Da testo, a stringa json formattata
            storicoinquinamentoapi = json.dumps(storicoinquinamentoapi)
        # Lo rende una response http
        response = make_response(storicoinquinamentoapi)
        # Il filename è inutile, però va bene perchè rende consistenti client e
        # server (?)
        response.headers['Content-Disposition'] = "attachment; filename=storico." + \
            str(formato)
        response.mimetype = "text/" + str(formato)  # Dice il tipo di file
        print(response)
        print(response.headers)
        return response

    @app.route("/aggiungiIrrigatore", methods=["POST", "GET"])
    def aggiungiIrrigatore():
        '''Permette l'aggiunta di un irrigatore ad un utente'''
        if request.method == "POST":
            richiesta = request.get_json()
            idTerreno = richiesta.get("idTerreno")
            nomeIrrigatore = richiesta.get("nomeIrrigatore")
            posizioneIrrigatore = richiesta.get("posizioneIrrigatore")
            idTerreno = AmbienteAgricoloService.aggiungiIrrigatore(
                idTerreno, nomeIrrigatore, posizioneIrrigatore)
            return jsonify({"risposta": "true", "idIrrigatore": idTerreno})

    @app.route("/getIrrigatore", methods=["POST", "GET"])
    def getIrrigatore():
        '''Permette la visualizzazione di tutti gli irrigatori presenti su un terreno'''
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            irrigatore = AmbienteAgricoloService.getIrrigatore(idIrrigatore)
            return jsonify({"idIrrigatore": irrigatore.id, "nomeIrrigatore": irrigatore.nome,
                           "posizioneIrrigatore": irrigatore.posizione})

    @app.route("/modificaIrrigatore", methods=["POST", "GET"])
    def modificaIrrigatore():
        '''Permette la modifica dei dati di un irrigatore'''
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            nomeIrrigatore = richiesta.get("nomeIrrigatore")
            posizioneIrrigatore = richiesta.get("posizioneIrrigatore")
            AmbienteAgricoloService.modificaIrrigatore(
                idIrrigatore, nomeIrrigatore, posizioneIrrigatore)
            return jsonify({"risposta": "true"})

    @app.route("/visualizzaIrrigatori", methods=["POST", "GET"])
    def visualizzaIrrigatori():
        '''Permette la visualizzazionde di tutti gli irrigatori di un terreno'''
        if request.method == "POST":
            richiesta = request.get_json()
            idTerreno = richiesta.get("idTerreno")
            irrigatori = AmbienteAgricoloService.visualizzaListaIrrigatori(
                idTerreno)
            return jsonify(irrigatori)

    @app.route("/eliminaIrrigatore", methods=["POST", "GET"])
    def eliminaIrrigatore():
        '''Permette l'eliminazione di un irrigatore'''
        if request.method == "POST":
            richiesta = request.get_json()
            idIrrigatore = richiesta.get("idIrrigatore")
            AmbienteAgricoloService.eliminaIrrigatore(idIrrigatore)
            return jsonify({"risposta": "true"})

    @app.route("/attivaDisattivaIrrigatore", methods=["POST", "GET"])
    def attivaDisattivaIrrigatore():
        '''Permette l'attivazione e la disattivazione di un irrigatore'''
        if request.method == "POST":
            richiesta = request.get_json()
            print(richiesta)
            idIrrigatore = richiesta.get("idIrrigatore")
            risposta = AmbienteAgricoloService.attivaDisattivaIrrigatore(
                idIrrigatore)
            if risposta:
                return jsonify({"risposta": "attivato"})
            else:
                return jsonify({"risposta": "disattivato"})

    """
    @app.route("/visualizzaEventi", methods=["POST", "GET"])
    def visualizzaEventi():
        if request.method == "POST":
            richiesta = request.get_json()
            idTerreno = richiesta.get("idTerreno")
            eventi = AmbienteAgricoloService.visualizzaListaEventi(idTerreno)
            return jsonify(eventi)
    """

    @app.route("/visualizzaTerreni", methods=["POST", "GET"])
    @login_required
    def visualizzaTerreni():
        '''Permette la visualizzazione di tutti i terreni di proprietà di utente farmer'''
        if current_user.ruolo != "farmer":
            farmer = AutenticazioneService.AutenticazioneService.getDatoreFromDipendente(
                current_user.id)
        else:
            farmer = current_user.id
        listaTerreni = AmbienteAgricoloService.visualizzaTerreni(farmer)

        return render_template("visualizzaTerreni.html",
                               listaTerreni=listaTerreni)

    @app.route("/visualizzaPredizioneIrrigazione", methods=["POST", "GET"])
    def visualizzaPredizioneIrrigazione():
        '''Permette la visualizzazione della predizione di irrigazione fornita dal modulo AI'''
        # get json request
        richiesta = request.get_json()
        id_terreno = richiesta.get("id_terreno")
        terreno = AmbienteAgricoloService.trovaTerreno(id_terreno)
        lat = AmbienteAgricoloService.cercalat(id_terreno)
        lon = AmbienteAgricoloService.cercalon(id_terreno)
        coltura = terreno.coltura
        stadio_crescita = terreno.stadio_crescita

        return jsonify(AmbienteAgricoloService.restituisciPredizioneLivelliIrrigazione(
            lon, lat, coltura, stadio_crescita))
