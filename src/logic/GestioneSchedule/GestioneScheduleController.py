from flask import jsonify, request
from src import app
from src.logic.GestioneSchedule.GestioneScheduleService import GestioneScheduleService

class GestioneScheduleController:
    
    @app.route("/schedule", methods=["GET", "POST"])
    def restituisciSchedule():
        """
            Questo metodo restituisce lo schedule settimanale di un terreno
        """
        #get json from request
        json = request.get_json()
        schedule_settimanale = GestioneScheduleService.trovaScheduleTerreno(json.get("id_terreno"))
        return jsonify(schedule_settimanale)
    
    @app.route(("/modificaLivelloSchedule"), methods=["POST"])
    def modificaLivelloSchedule():
        json = request.get_json()
        id_terreno = json.get("id_terreno")
        data = json.get("data")
        modalita = json.get("livello")
        
        GestioneScheduleService.modificaLivelloSchedule(id_terreno, data, modalita)
        
        return jsonify({"success": True})