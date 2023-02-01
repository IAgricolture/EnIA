from datetime import datetime
from flask import jsonify, request
from src import app
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
from src.logic.GestioneSchedule.GestioneScheduleService import GestioneScheduleService
from src.logic.model.Evento import Evento


class GestioneScheduleController:

    '''
    Classe Controller di Schedule

    ...

    Attributi
    ----------
    None

    Metodi
    -------
    restituisciSchedule():
        Questo metodo restituisce lo schedule settimanale di un terreno
    modificaLivelloSchedule():
        Questo metodo modifica lo schedule settimanale di un terreno
    usaScheduleConsigliato():
        Questo metodo va a settare uno schedule consignato dall analisi delle previsioni meteo

    '''

    @app.route("/schedule", methods=["GET", "POST"])
    def restituisciSchedule():
        '''
            Questo metodo restituisce lo schedule settimanale di un terreno
        '''
        # get json from request
        json = request.get_json()
        schedule_settimanale = GestioneScheduleService.trovaScheduleTerreno(
            json.get("id_terreno"))
        return jsonify(schedule_settimanale)

    @app.route(("/modificaLivelloSchedule"), methods=["POST"])
    def modificaLivelloSchedule():
        '''Questo metodo modifica lo schedule settimanale di un terreno'''
        json = request.get_json()
        id_terreno = json.get("id_terreno")
        data = json.get("data")
        modalita = json.get("livello")

        GestioneScheduleService.modificaLivelloSchedule(
            id_terreno, data, modalita)
        evento = Evento(
            "",
            "Scheduling",
            "Livello di irrigazione modificato per la data " +
            data +
            " con la modalità " +
            modalita,
            datetime.now(),
            "Scheduling",
            False,
            False,
            id_terreno)
        print(evento)
        GestioneEventiService.creaEvento(evento)
        return jsonify({"success": True})

    @app.route(("/usaSchedulingConsigliato"), methods=["POST"])
    def usaScheduleConsigliato():
        '''Questo metodo va a settare uno schedule consignato dall analisi delle previsioni meteo'''
        json = request.get_json()
        id_terreno = json.get("id_terreno")
        lat = json.get("lat")
        lon = json.get("lon")
        stadio = json.get("stadio")
        coltura = json.get("coltura")
        GestioneScheduleService.usaSchedulingConsigliato(
            id_terreno, lat, lon, stadio, coltura)
        schedule_settimanale = GestioneScheduleService.trovaScheduleTerreno(
            json.get("id_terreno"))
        return jsonify(schedule_settimanale)
